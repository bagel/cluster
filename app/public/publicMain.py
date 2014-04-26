import sys
import os
import urlparse
import urllib2
import json
import script
import login
import web
import httplib
import dpool
import gevent
import util
import socket
import threading
import auth
import re

class Public(object):
    def __init__(self, environ):
        self.environ = environ


class Home(Public):
    def __init__(self, environ):
        super(Home, self).__init__(environ)

    def response(self):
        return web.execute(self.environ, ("app/mon/",))


class Util(Public):
    def __init__(self, environ):
        super(Util, self).__init__(environ)

    @web.response
    def response(self):
        return ("text/html", web.template(self.environ, "util.html"))


class Online(Public):
    def __init__(self, environ):
        super(Online, self).__init__(environ)

    def _request(self, url, data='', headers={}):
        req = urllib2.Request(url=url)
        if data:
            req.add_data(data)
        if headers:
            for key, value in headers.item():
                req.add_header(key, value)
        return urllib2.urlopen(req, timeout=3).read()

    @web.response
    def online(self):
        ctype = 'text/plain; charset=utf-8'
        dpurl = 'http://dpadmin.grid.sina.com.cn/api/serverlist2.php?ip='
        wburl = 'http://w5.lb.sina.com.cn/api/api.php?action=info&realserver='
        ip = urlparse.parse_qs(self.environ['QUERY_STRING'])['ip'][0]
        admin = load = desp = port = 0
        dp_data = json.loads(self._request(url=dpurl+ip))
        if not dp_data['list']:
            return (ctype, 'null')
        dp_data = dp_data['list'][0]
        if int(dp_data['status']):
            admin = 1
        if dp_data['desp']:
            desp = 1
        if json.loads(self._request(url=wburl+dp_data['ip_in'])) or \
           json.loads(self._request(url=wburl+dp_data['ip_ex'])):
            load = 1
        try:
            if re.match('OK', self._request(url='http://%s' % ip)):
                port = 1
        except:
            pass
        response_body = json.JSONEncoder().encode({"admin": admin, "load": load, "desp": desp, "port": port})
        #response_body = '%d%d%d%d' % (admin, load, desp, port)
        return (ctype, response_body)


class Purge(Public):
    def __init__(self, environ):
        super(Purge, self).__init__(environ)

    def request(self, host, port, domain, uri, status):
        conn = httplib.HTTPConnection(host, port, timeout=15)
        try:
            conn.request("GET", uri, headers={"Host": domain, "X-Refresh": "do"})
            req = conn.getresponse()
            if req.status == 200 or req.status == 404:
                status["OK"].append(host)
            else:
                raise socket.timeout
        except socket.timeout:
            status["ERR"].append(host)

    def purge(self, domain, uri):
        hosts = dpool.get_serverlist("varnish")
        status = {"OK": [], "ERR": []}
        threads = []
        for host in hosts:
            threads.append(threading.Thread(target=self.request, args=(host, 8899, domain, uri, status)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return status

    @web.response
    def response(self):
        query = urlparse.parse_qs(self.environ["QUERY_STRING"])
        url = query.get("url", [""])[0]
        if not re.match('http://', url):
            url = 'http://' + url
        domain, uri = urllib2.splithost(url.lstrip('https:'))
        print domain, uri
        if not domain or not uri:
            status = ""
        else:
            user = auth.authdomain(self.environ, domain)
            if user != self.environ["USER"]:
                return user
            status = self.purge(domain, uri)
        if self.environ["HTTP_HOST"] == "api.dpool.cluster.sina.com.cn":
            return ("application/json", json.dumps(status))
        print status
        return ("text/html", web.template(self.environ, "purge.html", {"status": status, "user": self.environ["USER"], "key": util.userkey(self.environ["USER"])}))
