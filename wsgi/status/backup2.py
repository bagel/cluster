#!/usr/bin/env python

import sys
import os
import redis
import pymongo
import time
import re


r = redis.StrictRedis(host='10.13.32.21', port=6379)
db = pymongo.MongoClient("10.13.32.21", 2701)["hits"]

t0 = int(time.time())
t0 = t0 - t0 % 60

t = t0 = t0 - 86400 - 3600
while t > t0 - 3600 - 1200:
    print t
    t1 = time.time()

    day = time.strftime('%Y%m%d', time.localtime(t))

    data = []
    for k, v in r.hgetall(t).items():
        if re.match(r'\d+\.\d+\.\d+\.\d+', k):
            data.append({"host": k, "time": t, "hits": int(v)})
        else:
            data.append({"domain": k, "time": t, "hits": int(v)})
    r.delete(t)

    for key in r.keys("%s_*" % t):
        for k, v in r.hgetall(key).items():
            data.append({"host": key.split('_')[-1], "domain": k, "time": t, "hits": int(v)})
        r.delete(key)

    ct = db[day]
    if data:
        ct.insert(data)

    print time.time() - t1

    t -= 60

