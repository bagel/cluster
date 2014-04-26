#!/usr/bin/env python
#coding: utf-8

import sys
import os
import urllib2
import json
import re
import util

def node_info(mods, m=0):
    url = "http://dpadmin.grid.sina.com.cn/api/serverlist.php?mod=" + ','.join(mods)
    url_ip = "http://dpadmin.grid.sina.com.cn/api/serverlist2.php?ip="
    if m:
        url = "http://dpadmint.grid.sina.com.cn/api/serverlist.php?mod=" + ','.join(mods)
        url_ip = "http://dpadmint.grid.sina.com.cn/api/serverlist2.php?ip="

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
            info_idc[idc] = cn_name("idc", idc, m)
        if not info_mod.has_key(mod):
            info_mod[mod] = cn_name("mod", mod.split("-")[-1], m)
    return (info, info_idc, info_mod)

def cn_name(t, name, m=0):
    url = "http://dpadmin.grid.sina.com.cn/api/serverlist2.php?cn%s=" % t
    if m:
        url = "http://dpadmint.grid.sina.com.cn/api/serverlist2.php?cn%s=" % t
    return json.loads(urllib2.urlopen(url=url+name).read())["list"][0]["cn_name"]

def update():
    mods = ["dpool2_web", "dpool3_web", "ssoweb", "sso_wireless_web", "varnish", "blog_web"]
    node, idc, mod = node_info(mods)
    mods_m = ["cardweb", "cardsubsystem"]
    node_m, idc_m, mod_m = node_info(mods_m, m=1)
    for k_m, v_m in node_m:
        if node.has_key(k_m):
            for k2_m, v2_m in v_m:
                node[k_m][k2_m] = v2_m
    idc.update(idc_m)
    mod.update(mod_m)
    print node, idc, mod
    import redis
    r = redis.StrictRedis(util.localenv("REDIS_INFO_HOST"), util.localenv("REDIS_INFO_PORT"))
    r.hmset("info_node", node)
    r.hmset("info_idc", idc)
    r.hmset("info_mod", mod)


if __name__ == "__main__":
    update()
    #mods = ["dpool2_web", "dpool3_web", "ssoweb"]
    #node, idc, mod = node_info(mods)
    #print node, idc, mod
