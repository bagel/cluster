#!/usr/bin/env python
#coding: utf-8

import sys
import os
import urllib2
import urllib
import mc
import json
import time
import urlparse
import redis
import collections
import re
import web


class Status:
    def __init__(self, environ):
        self.ctype = "text/html"
        self.environ = environ
        self.query = urlparse.parse_qs(self.environ["QUERY_STRING"])
        self.r=redis.StrictRedis(host=self.environ["REDIS_STATUS_HOST"], port=int(self.environ["REDIS_STATUS_PORT"]))
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
            #ims = [ "-".join([idc, m]) for m in mods ]
            im = idc
        elif not idc and mod:
            caption = mod
            #ims = [ "-".join([i, mod]) for i in idcs ]
            im = mod
        elif not idc and not mod:
            caption = ""
            #ims = [ "-".join([i, m]) for i in idcs for m in mods ]
            im = "sum"
        else:
            caption = " ".join([idc, mod])
            #ims = [ "-".join([idc, mod]) ]
            im = "-".join([idc, mod])
        return (im, caption) 

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
        print "1:", time.time() -  t1
        im, caption = self.idcMod()
        print "2:", time.time() -  t1
        pipe = self.r.pipeline()
        domain = self.query.get("domain", ["sum"])[0]
        print "2.1:", time.time() - t1
        #keys = [ pipe.hget('-'.join([str(t + (i * offset)), im]), domain) for i in xrange(30 * m + 1) for im in ims ]
        keys = [ pipe.hget('-'.join([str(t + (i * offset)), im]), domain) for i in xrange(30 * m + 1) ]
        print "2.2:", time.time() - t1
        values = pipe.execute()
        print values
        caption = " ".join([caption, domain])
        print "3:", time.time() -  t1

        #sum ims values
        #p = len(im)
        v = len(values)
        print v
        for k in xrange(v):
            if values[k] == None:
                values[k] = 0
            else:
                values[k] = int(values[k])
        #if p > 1:
        #    values = [ sum(values[q:q+p]) for q in xrange(0, v, p) ]
        print "4:", time.time() -  t1

        #sum hits
        if qtime == "30min"  or qtime == "hour" or qtime == "4hour":
            sum_hits = sum(values)
        elif qtime == "week":
            sum_hits = sum(values) * 7 * 4
        else:
            sum_hits = sum(values) * 4
        if sum_hits > 100000000:
            sum_hits = u"%0.2f\u4ebf" % (int(sum_hits)/100000000.0)
        elif sum_hits > 10000:
            sum_hits = u"%0.2f\u4e07" % (int(sum_hits)/10000.0)
        else:
            sum_hits = str(sum_hits)

        #max hits
        max_hits = max(values)
        if (max_hits/60) > 100000000:
            max_hits_s = u"%0.2f\u4ebf" % (int(max_hits/60)/100000000.0)
        elif (max_hits/60) > 10000:
            max_hits_s = u"%0.2f\u4e07" % (int(max_hits/60)/10000.0)
        else:
            max_hits_s = str(max_hits / 60)

        #max time
        if xname == "week":
            max_time = time.strftime("%m/%d %H:%M", time.localtime(t - (30 * m + 1 - values.index(max_hits)) * offset))
        else:
            max_time = time.strftime("%H:%M", time.localtime(t - (30 * m + 1 - values.index(max_hits)) * offset))

        caption = " ".join([caption, max_time, max_hits_s, sum_hits])
        return (values, m, t, xname, offset, caption)

    @web.response
    def chartData(self):
        values, m, t, xname, offset, caption = self.data()

        #chart data 
        data = []
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
        #print "5:", time.time() -  t1


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

    @web.response
    def sum(self):
        qtime = self.query.get("time", [""])[0]
        t = time.time()
        if qtime:
            sum = self.r.hgetall(qtime)
        else:
            sum = {}
        print time.time() - t
        badkeys = set()
        for k, v in sum.iteritems():
            if not re.match('[\w\d\_\-\.]+$', k):
                badkeys.add(k)
            if int(v) < 1000:
                badkeys.add(k)
        for key in badkeys:
            sum.pop(key)
        return ("application/json", json.JSONEncoder().encode(sum))

    def dictHtml(self):
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
            "domains": list(self.domain),
            "user": self.environ["USER"],
        }
        return tdict

    @web.response
    def responseHtml(self, html, tdict):
        return (self.ctype, web.template(self.environ, html, tdict))

    def response(self):
        tdict = self.dictHtml()
        return self.responseHtml("status.html", tdict)

class StatusHigh(Status):
    def __init__(self, environ):
        Status.__init__(self, environ)

    def chartData(self):
        ctype = "application/json"
        t = time.time()
        data = self.r.hget("%d-sum" % (t - t % 60), "sum")
        if not data:
            data = 0
        chartdata = {
            "data": int(data)
        }
        response_body = json.JSONEncoder().encode(chartdata)
        return (ctype, response_body)

    def response(self):
        tdict = self.dictHtml()
        return self.responseHtml("high.html", tdict)

class StatusMap(Status):
    def __init__(self, environ):
        Status.__init__(self, environ)

    def mapData(self):
        ctype = "application/json"
        day = time.strftime('s%Y%m%d')

        province = {
            u'\u5b89\u5fbd': 'AH',
            u'\u798f\u5efa': 'FJ',
            u'\u7518\u8083': 'GS',
            u'\u5e7f\u4e1c': 'GD',
            u'\u8d35\u5dde': 'GZ',
            u'\u6d77\u5357': 'HA',
            u'\u6cb3\u5317': 'HB',
            u'\u9ed1\u9f99\u6c5f': 'HL',
            u'\u6cb3\u5357': 'HE',
            u'\u6e56\u5317': 'HU',
            u'\u6e56\u5357': 'HN',
            u'\u6c5f\u82cf': 'JS',
            u'\u6c5f\u897f': 'JX',
            u'\u5409\u6797': 'JL',
            u'\u8fbd\u5b81': 'LN',
            u'\u9752\u6d77': 'QH',
            u'\u9655\u897f': 'SA',
            u'\u5c71\u4e1c': 'SD',
            u'\u5c71\u897f': 'SX',
            u'\u56db\u5ddd': 'SC',
            u'\u4e91\u5357': 'YN',
            u'\u6d59\u6c5f': 'ZJ',
            u'\u897f\u85cf': 'XZ',
            u'\u5185\u8499\u53e4': 'NM',
            u'\u65b0\u7586': 'XJ',
            u'\u5e7f\u897f': 'GX',
            u'\u5b81\u590f': 'NX',
            u'\u5317\u4eac': 'BJ',
            u'\u91cd\u5e86': 'CQ',
            u'\u4e0a\u6d77': 'SH',
            u'\u5929\u6d25': 'TJ',
            u'\u6fb3\u95e8': 'MA',
            u'\u9999\u6e2f': 'HK',
            u'\u53f0\u6e7e': 'TA',
        }

        isp = {
            u'\u7535\u4fe1': 'CT',
            u'\u8054\u901a': 'CNC',
            u'\u79fb\u52a8': 'CM',
            u'\u94c1\u901a': 'CM',
            u'\u79fb\u901a': 'CM',
        }

        country = {
            u'\u4e2d\u56fd': 'CN',
        }

        dayData = self.r.hgetall(day)
        daySums = sum([ int(n) for n in dayData.values() ])

        provData = collections.Counter()
        ispData = collections.Counter()
        for k, v in dayData.iteritems():
            provData['.'.join(k.split('.')[:2])] += int(v)
            if re.match(r'\w+\.\w+.\w+', k):
                ispData[k.split('.')[2]] += int(v)
            else:
                ispData["RM"] += int(v)

        data = []
        for prov, sname  in province.iteritems():
            data.append({
                "id": "CN.%s" % sname,
                "displayValue": prov,
                "toolText": u"%s:%0.1f%%, \u7535\u4fe1:%0.1f%%, \u8054\u901a:%0.1f%%, \u79fb\u52a8:%0.1f%%" % (prov, float(provData.get("CN.%s" % sname, 0)) / daySums * 100, float(dayData.get("CN.%s.CT" % sname, 0)) / daySums * 100, float(dayData.get("CN.%s.CNC" % sname, 0)) / daySums * 100, float(dayData.get("CN.%s.CM" % sname, 0)) / daySums * 100),
                "value": provData.get("CN.%s" % sname, 0),
            })

        mapdata = {
            "caption": u"\u5168\u56fd:%d\u4e07 \u7535\u4fe1:%0.1f%% \u8054\u901a:%0.1f%% \u79fb\u52a8:%0.1f%% \u5176\u4ed6:%0.1f%% %s" % (daySums / 10000, float(ispData.get("CT", 0)) / daySums * 100, float(ispData.get("CNC", 0)) / daySums * 100, float(ispData.get("CM", 0)) / daySums * 100, float(ispData.get("RM", 0)) / daySums * 100, time.strftime("%Y/%m/%d")),
            "map": {
                "bordercolor": "005879",
                "fillcolor": "D7F4FF",
                "numbersuffix": "",
                "includevalueinlabels": "1",
                "labelsepchar": ":",
                "basefontsize": "9",
            },
            "colorRange": {
                "color": [
                    {
                        "minvalue": "0",
                        "maxvalue": "10000",
                        "code": "FFF8DC",
                    },
                    {
                        "minvalue": "10000",
                        "maxvalue": "1000000",
                        "code": "B8860B",
                    },
                    {
                        "minvalue": "1000000",
                        "maxvalue": "10000000",
                        "code": "008000",
                    },
                    {
                        "minvalue": "10000000",
                        "maxvalue": "100000000",
                        "code": "CD5C5C",
                    },
                ]
            },
            "data": data
        }
        response_body = json.JSONEncoder().encode(mapdata)
        return (ctype, response_body)

    def response(self):
        tdict = self.dictHtml()
        return self.responseHtml("map.html", tdict)

if __name__ == "__main__":
    data()
