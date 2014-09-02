#!/usr/bin/env python
#coding: utf-8

import sys
import os
import re
import redis
import time
import util2 as util


def mapData():
    r = redis.StrictRedis(host=util.localenv("REDIS_MAP_HOST"), port=int(util.localenv("REDIS_MAP_PORT")))
    datadir = os.path.join(util.localenv("DATA_DIR"), "hive")
    day = time.strftime("%Y%m%d")
    hivedir = os.path.join(datadir, "dpool_access_hits_%s" % day)
    hivefile = os.path.join(hivedir, os.listdir(hivedir)[0])
    fp = open(hivefile, "r")
    regex = re.compile('([\w\.\-]+)\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+([A-Z]+)\s+(\d+)')
    mapdata = {}
    while True:
        line = fp.readline()
        if not line:
            break
        result = re.match(regex, line)
        if not result:
            continue
        addData(mapdata, result.groups())

    yday = time.strftime("%Y%m%d", time.localtime(time.time() - 86400))
    r.hmset("map%s" % yday, mapdata)

def addData(mapdata, keys):
    domain, country, province, isp, timeflag, cnt = keys
    for d in [domain, "sum"]:
        if not mapdata.has_key(d):
            mapdata[d] = {}
        if not mapdata[d].has_key(country):
            mapdata[d][country] = {}
        if not mapdata[d][country].has_key(province):
            mapdata[d][country][province] = {}
        if not mapdata[d][country][province].has_key(isp):
            mapdata[d][country][province][isp] = {}
        if not mapdata[d][country][province][isp].has_key(timeflag):
            mapdata[d][country][province][isp][timeflag] = 0
        mapdata[d][country][province][isp][timeflag] += int(cnt)
        

if __name__ == "__main__":
    mapData()
