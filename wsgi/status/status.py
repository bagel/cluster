#!/usr/bin/env python
#coding: utf-8

import sys
import os
import script
import urllib2
import urllib
import mc
import json
import shortcut
import time
import urlparse
import redis


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

    def idcMod(self):
        idcs = self.idc.keys()
        mods = self.mod.keys()
        idc = self.query.get("idc", [""])[0]
        mod = self.query.get("mod", [""])[0]
        if idc and not mod:
            caption = idc
            ims = [ "-".join([idc, m]) for m in mods ]
        elif not idc and mod:
            caption = mod
            ims = [ "-".join([i, mod]) for i in idcs ]
        elif not idc and not mod:
            caption = ""
            ims = [ "-".join([i, m]) for i in idcs for m in mods ]
        else:
            caption = " ".join([idc, mod])
            ims = [ "-".join([idc, mod]) ]
        return (ims, caption) 

    def data(self):
        t = int(time.time())
        t1 = time.time()
        qtime = self.query.get("time", ["30min"])[0]
        if qtime == "30min":
            offset = 60
            m = 1            
            xname = "30 minutes"
        elif qtime == "hour":
            offset = 60
            m = 2
            xname = "hour"
        elif qtime == "4hour":
            offset = 60
            m = 4
            xname = "4 hours"
        elif qtime == "day":
            offset = 240
            m = 12
            xname = "day"
        elif qtime == "week":
            offset = 240 * 7
            m = 12
            xname = "week"
        else:
            t = int(time.mktime(time.strptime(qtime, "%Y-%m-%d"))) + 86400
            offset = 240
            m = 12
            xname = qtime

        t = t - t % offset - 30 * m * offset
        data = []
        print "1:", time.time() -  t1
        ims, caption = self.idcMod()
        print "2:", time.time() -  t1
        pipe = self.r.pipeline()
        domain = self.query.get("domain", ["sum"])[0]
        print "2.1:", time.time() - t1
        keys = [ pipe.hget('-'.join([str(t + (i * offset)), im]), domain) for i in xrange(30 * m + 1) for im in ims ]
        print "2.2:", time.time() - t1
        values = pipe.execute()
        caption = " ".join([caption, domain])
        print "3:", time.time() -  t1

        #sum ims values
        p = len(ims)
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
                if xname == "week":
                    data.append({"label": time.strftime("%m/%d %H:%M", time.localtime(t)), "value": str(int(n)/60), "tooltext": "%s, %s" % (time.strftime("%m/%d %H:%M", time.localtime(t)), str(int(n)/60))})
                else:
                    data.append({"label": time.strftime("%H:%M", time.localtime(t)), "value": str(int(n)/60), "tooltext": "%s, %s" % (time.strftime("%H:%M", time.localtime(t)), str(int(n)/60))})
            else:
                if xname == "week":
                    data.append({"value": str(int(n)/60), "tooltext": "%s, %s" % (time.strftime("%m/%d %H:%M", time.localtime(t)), str(int(n)/60))})
                else:
                    data.append({"value": str(int(n)/60), "tooltext": "%s, %s" % (time.strftime("%H:%M", time.localtime(t)), str(int(n)/60))})
            j += 1
            t += offset
        print "5:", time.time() -  t1

        max_hits = max(values)
        if xname == "week":
            max_time = time.strftime("%m/%d %H:%M", time.localtime(t - (30 * m + 1 - values.index(max_hits)) * offset))
        else:
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
        times = ["30min", "hour", "4hour", "day", "week"]
        t = time.time()
        for i in xrange(1, 7):
            times.append(time.strftime("%Y-%m-%d", time.localtime(t - i * 86400)))
        
        tdict = {
            "query_string": self.environ["QUERY_STRING"],
            "qdomain": self.query.get("domain", [""])[0],
            "qip": self.query.get("ip", [""])[0],
            "qidc": self.query.get("idc", [""])[0],
            "qmod": self.query.get("mod", [""])[0],
            "qtime": self.query.get("time", [""])[0],
            "idc": self.idc, 
            "mod": self.mod,
            "times": times,
            "domains": list(self.domain)
        }
        return (self.ctype, script.response(os.path.join(self.template, "status.html"), tdict))


if __name__ == "__main__":
    data()
