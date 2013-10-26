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


class Mon:
    def __init__(self, environ, template):
        self.environ = environ
        self.template = template
        self.config = json.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "config")))
        self.mods = self.config["pool_vip"].keys()
        self.idcs = self.config["idc"]
        self.net_idc = self.config["net_idc"]
        self.idc_gm = self.config["idc_gm"]
        self.pool_vip = self.config["pool_vip"]
        self.items = ["cpu_idle", "mem_free", "hits"]

    def body(self, temp, data):
        return script.response(os.path.join(self.template, temp), data)

    def stats(self, ip, module, idc):
        stat = []
        for item in self.items:
            url="http://%s/exmon/graph.php?r=5m&c=dpool-%s-%s&h=%s&m=%s&vl=%%25&json=1" % (self.idc_gm[idc], self.net_idc[".".join(ip.split(".")[:3])], module.title(), str(shortcut.outip(ip)), item)
            try:
                stat.append(json.loads(urllib2.urlopen(url).read())[0]["datapoints"][-3][0])
            except:
                stat.append(-1)
        if stat[0] < 20 or stat[1] <=0:
            stat.append(["btn-warning", "警告"])
        else:
            stat.append(["btn-success", "良好"])
        return stat

    def status_ip(self, ip, module, idc):
        data = {"ip": str(shortcut.outip(ip)), "module": module, "net_idc": self.net_idc[".".join(ip.split(".")[:3])], "gmond": self.idc_gm[idc], "mods": self.mods, "idcs": self.idcs, "idc": idc, "stat": self.stats(ip, module, idc)}
        return self.body("ip.html", data)

    def status_md(self, module, idc):
        md_ips = shortcut.load(self.pool_vip[module][idc][0])
        if not md_ips:
            return "error"
        md_stat = {}
        for ip in md_ips:
            md_stat.update({ip: self.stats(ip, module, idc)})
        data = {"md_stat": md_stat, "mods": self.mods, "idcs": self.idcs, "module": module, "idc": idc}
        return self.body("md.html", data)

class Mon_web2(Mon):
    def __init__(self, environ, template):
        Mon.__init__(self, environ, template)
        self.items = ["cpu_idle", "mem_free", "hits", "httpd"]

class Mon_web3(Mon):
    def __init__(self):
        Mon.__init__(self)
        self.items = ["cpu_idle", "mem_free", "hits", "interest.mix.sina.com.cn_active_processes"]

class Response:
    def __init__(self, environ, template):
        self.ctype = "text/html"
        self.environ = environ
        self.template = template
        self.query = urlparse.parse_qs(self.environ["QUERY_STRING"])

    def response(self):
        ip = module = idc = ""
        if self.query.has_key("ip"):
            ip = self.query["ip"][0]
        if self.query.has_key("module"):
            module = self.query["module"][0]
        if self.query.has_key("idc"):
            idc = self.query["idc"][0]
        if module and idc and ip:
            return (self.ctype, Mon_web2(self.environ, self.template).status_ip(ip, module, idc))
        elif module and idc:
            return (self.ctype, Mon_web2(self.environ, self.template).status_md(module, idc))
        else:
            module = "web2"
            idc = "tc"
            return (self.ctype, Mon_web2(self.environ, self.template).status_md(module, idc))
