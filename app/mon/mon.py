#!/usr/bin/env python
#coding: utf-8

import sys
import os
import script
import urllib2
import mc
import json
import shortcut
import time
import urlparse
import redis
import uwsgi
import urlparse


class Mon:
    def __init__(self, environ, template):
        self.ctype = "text/html"
        self.environ = environ
        self.template = template
        self.r=redis.StrictRedis(host=self.environ["REDIS_HOST"], port=6380, socket_timeout=5)
        self.channel = urlparse.parse_qs(self.environ['QUERY_STRING']).get('channel', ['sum'])[0]
        self.num = int(urlparse.parse_qs(self.environ['QUERY_STRING']).get('num', [50])[0])
        self.start = int(urlparse.parse_qs(self.environ['QUERY_STRING']).get('start', [0])[0])

    def chartData(self):
        ctype = "application/json"
        data = self.r.hget("sum_500", str(int(time.time())))
        if not data:
            data = 0
        chartdata = {
            "data": int(data)
        }
        response_body = json.JSONEncoder().encode(chartdata)
        return (ctype, response_body)

    def wsData(self):
        uwsgi.websocket_handshake(self.environ['HTTP_SEC_WEBSOCKET_KEY'], self.environ.get('HTTP_ORIGIN', ''))
        codes = []
        while True:
            t = str(int(time.time()))
            legend = []
            data = []
            keys = sorted(self.r.keys("sum_*"))
            for code in codes:
                key = '_'.join(["sum", code])
                legend.append("")
                if self.r.hexists(key, t):
                    data.append(int(self.r.hget(key, t)))
                else:
                    data.append(0)
            for key in keys:
                code = key.split('_')[-1]
                if self.r.hexists(key, t) and code not in codes:
                    codes.append(code)
                    data.append(int(self.r.hget(key, t)))
                    legend.append(code)
            if not data:
                time.sleep(2)
                continue
            wsdata = {
                "data": data,
                "legend": legend
            }
            uwsgi.websocket_send(json.JSONEncoder().encode(wsdata))
            time.sleep(2)

    def wsSubData(self):
        """Websocket subscribe redis pubsub"""
        uwsgi.websocket_handshake(self.environ['HTTP_SEC_WEBSOCKET_KEY'], self.environ.get('HTTP_ORIGIN', ''))
        channel = self.r.pubsub()
        channel.subscribe(self.channel)
        channel.parse_response()
        while True:
            try:
                wsdata = channel.parse_response()[2]
            except:
                time.sleep(1)
                wsdata = ''
                channel.subscribe(self.channel)
                channel.parse_response()
            uwsgi.websocket_send(wsdata)

    def wsSubData_nb(self):
        """Websocket subscribe redis pubsub nonbolocking.
           Keepalive websocket connection with client."""
        uwsgi.websocket_handshake(self.environ['HTTP_SEC_WEBSOCKET_KEY'], self.environ.get('HTTP_ORIGIN', ''))
        channel = self.r.pubsub()
        channel.subscribe(self.channel)
        channel.parse_response()
        websocket_fd = uwsgi.connection_fd()
        redis_fd = channel.connection._sock.fileno()
        while True:
            uwsgi.wait_fd_read(websocket_fd, 3)
            uwsgi.wait_fd_read(redis_fd)
            uwsgi.suspend()
            fd = uwsgi.ready_fd()
            if fd > -1:
                if fd == websocket_fd:
                    uwsgi.websocket_recv_nb()
                elif fd == redis_fd:
                    wsdata = channel.parse_response()[2]
                    uwsgi.websocket_send(wsdata)
            else:
                uwsgi.websocket_recv_nb()
                time.sleep(1)

    def LogAccess(self):
        return ("application/json", json.JSONEncoder().encode(self.r.zrevrangebyscore(self.channel, "+inf", 0, start=self.start, num=self.num)))

    def LogError(self, num=50):
        return ("application/json", json.JSONEncoder().encode(self.r.zrevrangebyscore('_'.join([self.channel, "err"]), "+inf", 0, start=self.start, num=self.num)))

    def LogAccessCount(self):
        return ("application/json", json.JSONEncoder().encode({"count": self.r.zcount(self.channel, "-inf", "+inf")}))

    def LogErrorCount(self):
        return ("application/json", json.JSONEncoder().encode({"count": self.r.zcount('_'.join([self.channel, "err"]), "-inf", "+inf")}))

    def response(self):
        if self.channel == "sum":
            title = ""
        else:
            title = self.channel
        return (self.ctype, script.response(os.path.join(self.template, "mon.html"), {"user": self.environ["USER"], "channel": self.channel, "title": title}))
 
