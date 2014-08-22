import sys
import os
import redis
import urlparse
import time
import web
import json



class High(object):
    def __init__(self, environ):
        self.ctype = "text/html"
        self.environ = environ
        self.query = urlparse.parse_qs(self.environ["QUERY_STRING"])
        self.r = redis.StrictRedis(host=web.getenv("REDIS_STATUS_TEST_HOST"), \
                                   port=int(web.getenv("REDIS_STATUS_TEST_PORT")))
        self.r_info = redis.StrictRedis(host=web.getenv("REDIS_INFO_HOST"), \
                                       port=int(web.getenv("REDIS_INFO_PORT")))
        self.qdomain = self.query.get("domain", ["sum"])[0]
        self.qdate = self.query.get("date", ["day"])[0]
        self.qidc = self.query.get("idc", [""])[0]
        self.qmod = self.query.get("mod", [""])[0]
        self.qrtime = self.query.get("rtime", [""])[0]
        self.quri = self.query.get("uri", [""])[0]
        self.qurl = self.query.get("url", [""])[0]

    def queryKey(self):
        """redis key suffix by idc and mod, defualt sum"""
        if not self.qidc and not self.qmod:
            return "sum"
        else:
            return '-'.join([v for v in [self.qidc, self.qmod] if v])

    def queryTime(self):
        """return offset, start time and dots number by qdate"""
        t = int(time.time())
        start = lambda x, y, z: x - x%y - z*y
        if self.qdate == "30min":
            return (60, start(t, 60, 30), 30)
        elif self.qdate == "hour":
            return (60, start(t, 60, 60), 60)
        elif self.qdate == "4hour":
            return (60, start(t, 60, 240), 240)
        elif self.qdate == "day":
            return (240, start(t, 240, 360), 360)
        elif self.qdate == "week":
            return (240*7, start(t, 240*7, 360), 360)
        else:
            t = int(time.mktime(time.strptime(self.qdate, "%Y-%m-%d"))) + 86400
            return (240, start(t, 240, 360), 360)

    @web.response
    @web.util.tracefunc
    def chartData(self):
        """chart data, [offset, start time, [{name: data}, ...]]"""
        ctype = "application/json"
        qkey = self.qurl
        print qkey
        data = self.r.hgetall(qkey)
        data_keys = [ int(dk) for dk in data.iterkeys() ]
        data_keys.sort()
        start = data_keys[0]
        offset = data_keys[1] - data_keys[0]
        num = len(data_keys)
        values = [ data[str(k)] for k in data_keys ]
        chartdata = [offset, start, [{"day": values}]]
        response_body = json.JSONEncoder().encode(chartdata)
        return (ctype, response_body)

    @web.response
    def testData(self):
        ctype = "application/json"
        url = self.quri
        chartdata = {"title": url, "data": []}
        for i in xrange(1, 4):
            day_y = time.strftime("%Y%m%d", time.localtime(time.time() - 86400 * i))
            url_y = "%s_%s" % (url, day_y)
            key = "card.weibo.com_%s" % url
            key_y = "%s_%s" % (day_y, key)
            data_y =  eval(self.r.get(key_y))[2:-2]
            data_y_new = []
            for d in data_y:
                d[0] = str(int(d[0]) + 86400 * (i - 1))
                data_y_new.append(d)
            chartdata["data"].append({day_y: data_y_new})
        response_body = json.JSONEncoder().encode(chartdata)
        return (ctype, response_body)

    @web.response
    @web.util.tracefunc
    def response(self):
        dates = ["30min", "hour", "4hour", "day", "week"]
        t = time.time()
        for i in xrange(1, 7):
            dates.append(time.strftime("%Y-%m-%d", time.localtime(t - \
                                       i * 86400)))

        domain_status = self.r_info.hget("info_domain_status", self.qdomain)
        if domain_status:
            domain_status = eval(domain_status)
        else:
            domain_status = {}

        rtime_title = ''
        if self.qrtime:
            rtime_title = self.qrtime.replace('_', '~') + 's'

        tdict = {
            "query_string": self.environ["QUERY_STRING"],
            "qdomain": self.query.get("domain", [""])[0],
            "qdate": self.query.get("date", [""])[0],
            "qidc": self.qidc,
            "qmod": self.qmod,
            "qrtime": self.qrtime,
            "quri": self.quri,
            "idc": self.r_info.hgetall("info_idc"),
            "mod": self.r_info.hgetall("info_mod"),
            "dates": dates,
            "title": ' '.join([ v for v in [self.qidc, self.qmod, \
                                self.qdomain, self.quri, self.qurl, rtime_title] if v ]),
            "domain_status": domain_status,
            "domain_uri_rtime": json.dumps(domain_status.get("uri_rtime", {})),
        }

        return (self.ctype, web.template(self.environ, "high_test.html", tdict))


