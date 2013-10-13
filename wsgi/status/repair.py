#!/usr/bin/env python

import sys
import os
import time
import redis

r = redis.StrictRedis(host='10.13.32.21', port=6379)

day = time.strftime("%Y/%m/%d")

if len(sys.argv) < 3:
    sys.exit(0)

n = sys.argv[1]
m = sys.argv[2]

nt = int(time.mktime(time.strptime(' '.join([day, n]), "%Y/%m/%d %H:%M")))
mt = int(time.mktime(time.strptime(' '.join([day, m]), "%Y/%m/%d %H:%M")))

print nt, mt
p = r.pipeline()
for key in r.keys('%s-*' % nt):
    p.hmset(key.replace(str(nt), str(mt)), r.hgetall(key))

p.execute()
