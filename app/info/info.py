#!/usr/bin/env python

import sys
import os
import script
import redis
import urlparse
import json
import urllib2
import ConfigParser
import re
import socket
import time
import login


class Info:
    def __init__(self, environ, template):
        self.ctype = "text/html"
        self.environ = environ
        self.template = template
        self.query = urlparse.parse_qs(self.environ["QUERY_STRING"])
        self.r=redis.StrictRedis(host='10.13.32.21', port=6379)
        #self.node = eval(self.r.get("node"))
        #self.idc = eval(self.r.get("idc"))
        #self.mod = eval(self.r.get("mod"))
        #self.domain = eval(self.r.get("domain"))

    def response(self):
        return (self.ctype, script.response(os.path.join(self.template, "info.html"), {"user": self.environ["USER"]}))

class InfoData(Info):
    def __init__(self, environ, template):
        Info.__init__(self, environ, template)
        self.ctype = "application/json"
        self.region = ['mars', 'apollo', 'atlas']

    def ispData(self, vip):
        isp = self.r.hget('isp', vip)
        if isp:
            return isp
        url = 'http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=' + vip
        isp = json.loads(urllib2.urlopen(url, timeout=3).read())["isp"]
        self.r.hset('isp', vip, isp)
        return isp

    def confData(self, conf):
        url = 'http://dpadmin.grid.sina.com.cn/api/fetch_newestfile.php?title=' + conf
        return urllib2.urlopen(url, timeout=3)

    def poolData(self, domain):
        config = ConfigParser.ConfigParser()
        config.readfp(self.confData("web3_varnish"))
        if domain in config.get("web3", "domains").strip().split(' '):
            return "web3"
        else:
            return "web2"

    def dnsData(self, domain, pool):
        dns = eval(self.r.hget("info_dns", domain))
        data = {}
        for vip in dns:
            vipData = self.r.hget("info_vip", vip)
            if not vipData:
                continue
            data[vip] = eval(vipData)
            member = data[vip]["member"]
            memberNew = {}
            for poolname, servers in member.iteritems():
                if pool == "web3" and poolname == "dpool2_web":
                    continue
                if re.match('dpool\d+_web', poolname):
                    poolname = "web"
                if not memberNew.has_key(poolname):
                    memberNew[poolname] = []
                memberNew[poolname].extend(servers)
            if memberNew.has_key("varnish") and not memberNew.has_key("web"):
                memberNew["web"] = eval(self.r.hget("info_backend", pool))[data[vip]["idc"]]
                cache = "true"
            else:
                cache = "false"
            data[vip]["member"] = memberNew
        return (data, cache)

    def response(self):
        t = time.time()
        auth = login.user(self.environ)
        if auth != 1:
            return auth
        domain = self.query['domain'][0]
        servername = self.r.hget("info_domainalias", domain)
        data = {}
        print "1:", time.time() - t
        data["domain"] = domain
        data.update(eval(self.r.hget("info_vhost", servername)))
        print "2:", time.time() - t
        data["vip"], data["cache"] = self.dnsData(domain, data["pool"])
        print "3:", time.time() - t
        return (self.ctype, json.JSONEncoder().encode(data))


if __name__ == "__main__":
    t = time.time()
    InfoData("", "").response()
    print time.time() - t
