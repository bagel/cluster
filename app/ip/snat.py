#!/usr/bin/env python

import sys
import os
import redis
import urllib2
import json
import re

sys.path.append('/data1/www/htdocs/api.dpool.cluster.sina.com.cn/lib')
import shortcut


r = redis.StrictRedis('10.13.32.21')

node = eval(r.get('node'))

snat = {}
for k, v in node.iteritems():
    idc = {}
    for m, ips in v.iteritems():
        if m != "dpool2_web" and m != "dpool3_web":
            continue
        mod = set()
        for ip in ips:
            print mod
            ip_snat = shortcut.snat(ip)
            if re.match('\d+\.\d+\.\d+\.\d+', ip_snat):
                mod.add(ip_snat.strip())
        idc[m] = list(mod)
    if not idc:
        continue
    snat[k] = idc

r.set("snat", snat)
