#!/usr/bin/env python

import os
import sys
import redis
import json
import urllib2
import re
import ConfigParser
import util

def vipData(server):
    url = 'http://w5.lb.sina.com.cn/api/api.php?action=info&realserver=' + server
    data = json.loads(urllib2.urlopen(url).read())
    vip = set()
    for d in data:
        if re.search("ssl", d["poolname"]):
            continue
        for v in d["virtualaddress"].strip().split(','):
            if re.search(r':80$', v) or re.search(r':8899$', v):
                vip.add(re.sub(r'(\d+\.\d+\.\d+\.\d+):80', r'\1', v))
    return vip

def ispData(vip):
    url = 'http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=' + vip
    isp = json.loads(urllib2.urlopen(url, timeout=3).read()).get("isp", "")
    return isp

def getOutip(ip):
    url = 'http://dpadmin.grid.sina.com.cn/api/serverlist.php?ip=' + ip
    data = json.loads(urllib2.urlopen(url, timeout=3).read()).get("list", "")
    if not data:
        return 1
    else:
        return data[0]["ip_ex"]

def vipSet(): 
    r = redis.StrictRedis(util.localenv("REDIS_INFO_HOST"), util.localenv("REDIS_INFO_PORT"))
    node = r.hgetall("info_node")
    vip = {}
    for idc, pool in node.iteritems():
        pool = eval(pool)
        for poolname, servers in pool.iteritems():
            for server in servers:
                print server
                vips = vipData(server)
                for v in vips:
                    if not vip.has_key(v):
                        vip[v] = {}
                        vip[v]["idc"] = idc
                        vip[v]["isp"] = ispData(v)
                    if not vip[v].has_key("member"):
                        vip[v]["member"] = {}
                    if not vip[v]["member"].has_key(poolname):
                        vip[v]["member"][poolname] = []
                    if server not in vip[v]["member"][poolname]:
                        vip[v]["member"][poolname].append(server)

                serverOut = getOutip(server)
                if serverOut == 1:
                    continue
                vips = vipData(serverOut)
                for v in vips:
                    if not vip.has_key(v):
                        vip[v] = {}
                        vip[v]["idc"] = idc
                        vip[v]["isp"] = ispData(v)
                    if not vip[v].has_key("member"):
                        vip[v]["member"] = {}
                    if not vip[v]["member"].has_key(poolname):
                        vip[v]["member"][poolname] = []
                    if server not in vip[v]["member"][poolname]:
                        vip[v]["member"][poolname].append(server)

    if vip:
        print vip
        r.hmset("info_vip", vip)
    return vip


if __name__ == "__main__":
    #print vipData("10.13.32.23")
    vipSet()
