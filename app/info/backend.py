#!/usr/bin/env python

import sys
import os
import urllib2
import json
import redis
import ConfigParser
import util2 as util


def confData(conf):
    url = 'http://dpadmin.grid.sina.com.cn/api/fetch_newestfile.php?title=' + conf
    return urllib2.urlopen(url, timeout=3)

def backSet():
    r = redis.StrictRedis(util.localenv("REDIS_INFO_HOST"), util.localenv("REDIS_INFO_PORT"))
    config = ConfigParser.ConfigParser()
    config.readfp(confData("varnish_backend.conf"))
    data = {}
    for sec in config.sections():
        pool = sec.replace('dpool', 'web')
        data[pool] = {}
        for opt in config.options(sec):
            data[pool][opt] = []
            vip = r.hget("info_vip", config.get(sec, opt))
            if not vip:
                continue
            vip = eval(vip)
            for servers in vip['member'].values():
                data[pool][opt].extend(servers)

    if data:
        print data
        r.hmset("info_backend", data)


if __name__ == "__main__":
    backSet()
