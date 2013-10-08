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
t = t0 = t0 - 86400 - 3600
while t > t0 - 3600 - 1200:
    print t
    t1 = time.time()

    if t % 240 != 0:
        for key in r.keys("%s-*" % t):
            p.delete(key)

    print time.time() - t1

    t -= 60

p.execute()
