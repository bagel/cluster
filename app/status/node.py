#!/usr/bin/env python
#coding: utf-8

import sys
import os
import urllib2
import json
import re

def node_info(mods):
    url = "http://dpadmin.grid.sina.com.cn/api/serverlist.php?mod=" + ','.join(mods)
    url_ip = "http://dpadmin.grid.sina.com.cn/api/serverlist2.php?ip="
    info = {}
    info_idc = {}
    info_mod = {}
    for node in json.loads(urllib2.urlopen(url=url).read())["list"]:
        intip = node["ip_in"]
        idc = re.sub(r"([a-z]+)\d*", r"\1", node["section_id"])
        mod = "-".join([ n["mname"] for n in json.loads(urllib2.urlopen(url_ip + intip).read())["list"] ])
        if info.has_key(idc):
            if info[idc].has_key(mod):
                info[idc][mod].append(intip)
            else:
                info[idc][mod] = [intip]
        else:
            info[idc] = {mod: [intip]}
        if not info_idc.has_key(idc):
            info_idc[idc] = cn_name("idc", idc)
        if not info_mod.has_key(mod):
            info_mod[mod] = cn_name("mod", mod.split("-")[-1])
    return (info, info_idc, info_mod)

def cn_name(type, name):
    url = "http://dpadmin.grid.sina.com.cn/api/serverlist2.php?cn%s=" % type
    return json.loads(urllib2.urlopen(url=url+name).read())["list"][0]["cn_name"]

def update():
    mods = ["dpool2_web", "dpool3_web", "ssoweb", "sso_wireless_web", "varnish", "blog_web"]
    node, idc, mod = node_info(mods)
    import redis
    r = redis.StrictRedis("10.13.32.21")
    r.set("node", node)
    r.set("idc", idc)
    r.set("mod", mod)


if __name__ == "__main__":
    update()
    #mods = ["dpool2_web", "dpool3_web", "ssoweb"]
    #node, idc, mod = node_info(mods)
    #print node, idc, mod
