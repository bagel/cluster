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
import threading
import Queue


class Multi(threading.Thread):
    def __init__(self, pipe, keys, n, q):
        threading.Thread.__init__(self)
        self.pipe = pipe
        self.keys = keys
        self.n = n
        self.q = q

    def run(self):
        #[ self.pipe.hget(k, self.n) for k in self.keys ]
        for k in self.keys:
            self.pipe.hget(k, self.n)
        print "work"
        self.q.put(self.pipe.execute())

class Status:
    def __init__(self, environ, template):
        self.ctype = "text/html"
        self.environ = environ
        self.template = template
        self.query = urlparse.parse_qs(self.environ["QUERY_STRING"])
        self.r=redis.StrictRedis(host='10.13.32.21', port=6379)
        self.node = eval(self.r.get("node"))
        self.idc = eval(self.r.get("idc"))
        self.mod = eval(self.r.get("mod"))
        self.domain = eval(self.r.get("domain"))

    def sip(self):
        ips = []
        if self.query.has_key("ip"):
            ip = self.query["ip"][0]
            caption = ip
            ips.append(ip)
        else:
            if self.query.has_key("idc") and not self.query.has_key("mod"):
                idc = self.query["idc"][0]
                caption = idc
                for mod in self.mod.keys():
                    if self.node[idc].has_key(mod):
                        ips.extend(self.node[idc][mod])
            elif not self.query.has_key("idc") and self.query.has_key("mod"):
                mod = self.query["mod"][0]
                caption = mod
                for idc in self.idc.keys():
                    if self.node[idc].has_key(mod):
                        ips.extend(self.node[idc][mod])
            elif not self.query.has_key("idc") and not self.query.has_key("mod"):
                caption = time.strftime("%Y-%m-%d", time.localtime())
                for mod in self.mod.keys():
                    for idc in self.idc.keys():
                        if self.node[idc].has_key(mod):
                            ips.extend(self.node[idc][mod])
            else:
                idc = self.query["idc"][0]
                mod = self.query["mod"][0]
                caption = " ".join([idc, mod])
                if self.node[idc].has_key(mod):
                    ips.extend(self.node[idc][mod])
                else:
                    ips = ["0.0.0.0"]
        return (ips, caption)

    def data(self):
        t = int(time.time())
        t1 = time.time()
        if self.query.has_key("time"):
            if self.query["time"][0] == "30min":
                offset = 60
                m = 1            
                xname = "30 minutes"
            elif self.query["time"][0] == "hour":
                offset = 60
                m = 2
                xname = "hour"
            elif self.query["time"][0] == "4hour":
                offset = 60
                m = 4
                xname = "4 hours"
            elif self.query["time"][0] == "day":
                offset = 240
                m = 12
                xname = "day"
        else:
            offset = 60
            m = 1
            xname = "30 minutes"
        t = t - t % offset - 30 * m * offset
        data = []
        print "1:", time.time() -  t1
        ips, caption = self.sip()
        print "2:", time.time() -  t1
        if ips and not self.query.has_key("domain"):
            #values = self.r.mget([ "_".join([ip, str(t + (i * offset))]) for i in xrange(30 * m + 1) for ip in ips ])
            pipe = self.r.pipeline()
            print "2.5:", time.time() - t1
            [ pipe.hget(str(t + (i * offset)), ip) for i in xrange(30 * m + 1) for ip in ips ]
            print "2.6:", time.time() - t1
            values = pipe.execute()
        elif not ips and self.query.has_key("domain"):
            domain = self.query["domain"][0]
            caption = domain
            #values = self.r.mget([ "_".join([self.query["domain"][0], str(t + (i * offset))]) for i in xrange(30 * m + 1) ])
            pipe = self.r.pipeline()
            print "2.5:", time.time() - t1
            [ pipe.hget(str(t + (i * offset)), domain) for i in xrange(30 * m + 1) ]
            print "2.6:", time.time() - t1
            values = pipe.execute()
        elif ips and self.query.has_key("domain"):
            domain = self.query["domain"][0]
            #values = self.r.mget([ "_".join([ip, self.query["domain"][0], str(t + (i * offset))]) for i in xrange(30 * m + 1) for ip in ips ])
            pipe = self.r.pipeline()
            print "2.5:", time.time() - t1
            #[ pipe.hget("_".join([str(t + (i * offset)), ip]), domain) for i in xrange(30 * m + 1) for ip in ips ]
            keys = [ "_".join([str(t + (i * offset)), ip]) for i in xrange(30 * m + 1) for ip in ips ]
            print "2.6:", time.time() - t1
            [ pipe.hget(k, domain) for k in keys ]
            #n = len(keys) / 10000
            #values = []
            #thread = []
            #q = Queue.Queue()
            #for i in xrange(0, n + 1):
            #    t = Multi(pipe, keys[i*10000:(i+1)*10000], domain, q)
            #    t.start()
            #    thread.append(t)
            #for t in thread:
            #    t.join()
            #print q.get()
            print "2.7:", time.time() - t1
            values = pipe.execute()
            caption = " ".join([caption, domain])
        print "3:", time.time() -  t1

        #sum ips values
        p = len(ips)
        v = len(values)
        print v
        for k in xrange(v):
            if values[k] == None:
                values[k] = 0
            else:
                values[k] = int(values[k])
        if p > 1:
            values = [ sum(values[q:q+p]) for q in xrange(0, v, p) ]
        print "4:", time.time() -  t1
        
        j = 0
        while j <= (30 * m):
            n = values[j]
            if not n:
                n = 0
            if j % (3 * m) == 0:
                data.append({"vline": "true", "lineposition": "1", "color": "dddddd", "thickness": "1.5"})
                data.append({"label": time.strftime("%H:%M", time.localtime(t)), "value": str(int(n)/60), "tooltext": "%s, %s" % (time.strftime("%H:%M", time.localtime(t)), str(int(n)/60))})
            else:
                data.append({"value": str(int(n)/60), "tooltext": "%s, %s" % (time.strftime("%H:%M", time.localtime(t)), str(int(n)/60))})
            j += 1
            t += offset
        print "5:", time.time() -  t1

        max_hits = max(values)
        max_time = time.strftime("%H:%M", time.localtime(t - (30 * m + 1 - values.index(max_hits)) * offset))
        caption = " ".join([caption, max_time, str(max_hits / 60)])

        chartdata = {
            "chart": {
                "caption": caption,
                "xAxisName": xname,
                "yAxisName": "hits/s",
                "numberPrefix": "",
                "canvasPadding": "15",
                "chartRightMargin": "30",
                "linecolor": "0066cc",
                "labelDisplay": "NONE",
                "showValues": "0",
                "anchorAlpha": "0",
                "lineThickness": "2.5",
            },
            "data": data
        }
        return ("application/json", json.JSONEncoder().encode(chartdata))

    def response(self):
        tdict = {
            "query_string": self.environ["QUERY_STRING"], 
            "qdomain": self.query.get("domain", [""])[0],
            "qip": self.query.get("ip", [""])[0],
            "qidc": self.query.get("idc", [""])[0],
            "qmod": self.query.get("mod", [""])[0],
            "idc": self.idc, 
            "mod": self.mod,
            "domains": list(self.domain)
        }
        return (self.ctype, script.response(os.path.join(self.template, "status.html"), tdict))


if __name__ == "__main__":
    data()
