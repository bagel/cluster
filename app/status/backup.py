#!/usr/bin/env python

import sys
import os
import redis
import time
import re
import util2 as util


r = redis.StrictRedis(host=util.localenv("REDIS_STATUS_HOST"), port=int(util.localenv("REDIS_STATUS_PORT")))

t0 = int(time.time())
t0 = t0 - t0 % 60

p = r.pipeline()

#delete more than 4 hour not 4 min
t = t1 = t0 - 4 * 3600 - 3600
while t > t1 - 3600 - 1200 - 4 * 3600 - 86400:
    print t

    if t % 240 != 0:
        for key in r.keys("%s-*" % t):
            p.delete(key)

    t -= 60

#delete more than one week 4 min
t = t2 = t0 - 86400 * 7 - 3600
while t > t2 - 3600 - 1200 - 86400 * 7:
    print t
    if t % 240 == 0:
        for key in r.keys("%s-*" % t):
            p.delete(key)

    t -= 60

#sum 
t = t3 = t0
hour = time.strftime('%Y%m%d%H', time.localtime(t0 - 3600))
day = time.strftime('%Y%m%d', time.localtime(t0 - 3600))
while t > t3 - 3600:
    t -= 60
    print t
    for key in r.keys("%s-sum" % t):
        print key
        for d, h in r.hgetall(key).items():
            p.hincrby(hour, d, h)
            p.hincrby(day, d, h)

#delete more than one week everything
t = t4 = t0 - 86400 * 7
while t > t4 - 86400 * 7:
    for key in r.keys("%s*" % time.strftime("%Y%m%d", time.localtime(t))):
        print key
        p.delete(key)

    t -= 86400

t5 = time.time()
p.execute()
print t0, time.time() - t5
