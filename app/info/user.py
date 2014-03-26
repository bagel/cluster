#!/usr/bin/env python

import sys
import os
import redis

r = redis.StrictRedis("10.13.32.21")

if len(sys.argv) < 2:
    sys.exit(0)

user = sys.argv[1]
domain = sys.argv[2:]

for d in domain:
    r.hset("info_user", d, [user])
