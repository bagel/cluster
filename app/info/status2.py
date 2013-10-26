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
import pycurl
import redis


class Status:
    def __init__(self, environ, template):
        self.ctype = "text/html"
        self.environ = environ
        self.template = template
        self.query = urlparse.parse_qs(self.environ["QUERY_STRING"])

    def data(self):
        r=redis.StrictRedis(host='10.73.48.210', port=6379)
        t = int(time.time())
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
                offset = 120
                m = 4
                xname = "4 hours"
            elif self.query["time"][0] == "day":
                offset = 60
                m = 12
                xname = "day"
        else:
            offset = 60
            m = 1
            xname = "30 minutes"
        t = t - t % offset - 30 * m * offset
        data = []
        #print [ t + (i * offset) for i in xrange(30 * m + 1) ]
        j = 0
        while j <= (30 * m):
            if self.query.has_key("ip") and not self.query.has_key("domain"):
                n = r.get("_".join([self.query["ip"][0], str(t)]))
                caption = self.query["ip"][0]
            elif self.query.has_key("domain") and not self.query.has_key("ip"):
                n = r.get("_".join([self.query["domain"][0], str(t)]))
                caption = self.query["domain"][0]
            elif self.query.has_key("ip") and self.query.has_key("domain"):
                n = r.get("_".join([self.query["ip"][0], self.query["domain"][0], str(t)]))
                caption = "  ".join([self.query["ip"][0],  self.query["domain"][0]])
            else:
                n = r.get("10.73.48.26_" + str(t))
                caption = "10.73.48.26"

            if not n:
                n = 0
            if j % (3 * m) == 0:
                data.append({"vline": "true", "lineposition": "1", "color": "dddddd", "thickness": "1.5"})
                data.append({"label": time.strftime("%H:%M", time.localtime(t)), "value": str(int(n)/60), "showValue": "1"})
            else:
                data.append({"value": str(int(n)/60), "tooltext": "%s, %s" % (time.strftime("%H:%M", time.localtime(t)), str(int(n)/60))})
            j += 1
            t += offset

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
            },
            "data": data
        }
        return ("application/json", json.JSONEncoder().encode(chartdata))

    def response(self):
        return (self.ctype, script.response(os.path.join(self.template, "status.html"), {"query": self.environ["QUERY_STRING"]}))


if __name__ == "__main__":
    data()
