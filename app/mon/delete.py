#!/usr/bin/env python

import sys
import os
import redis
import time

r = redis.StrictRedis('10.13.32.21', 6380)
keys = r.keys('*')
t = int(time.time())

for key in keys:
    if len(key.split('_')) == 3:
        continue
    r.zremrangebyscore(key, '-inf', t - 10*3600)
