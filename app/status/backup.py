#!/usr/bin/env python

import sys
import os
import redis
import time
import re


r = redis.StrictRedis(host='10.13.32.21', port=6379)

t0 = int(time.time())
t0 = t0 - t0 % 60

p = r.pipeline()
t = t1 = t0 - 86400 - 3600
while t > t1 - 3600 - 1200:
    print t

    if t % 240 != 0:
        for key in r.keys("%s-*" % t):
            p.delete(key)

    t -= 60

t = t2 = t0 - 86400 * 7 - 3600
while t > t2 - 3600 - 1200:
    print t
    if t % 240 == 0:
        for key in r.keys("%s-*" % t):
            p.delete(key)

    t -= 60

t = t3 = t0
hour = time.strftime('%Y%m%d%H', time.localtime(t0 - 3600))
day = time.strftime('%Y%m%d', time.localtime(t0 - 3600))
while t > t3 - 3600:
    t -= 60
    print t
    for key in r.keys("%s-*" % t):
        print key
        for d, h in r.hgetall(key).items():
            p.hincrby(hour, d, h)
            p.hincrby(day, d, h)

t = t4 = t0 - 86400 * 7
while t > t4 - 86400:
    for key in r.keys("%s*" % time.strftime("%Y%m%d", time.localtime(t))):
        print key
        p.delete(key)

    t -= 86400

t5 = time.time()
p.execute()
print t0, time.time() - t5
