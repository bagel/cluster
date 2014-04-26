#!/usr/bin/env python

import sys
import os
import redis
import util

r = redis.StrictRedis(util.localenv("REDIS_INFO_HOST"), util.localenv("REDIS_INFO_PORT"))

if len(sys.argv) < 2:
    sys.exit(0)

user = sys.argv[1]
domain = sys.argv[2:]

for d in domain:
    r.hset("info_user", d, [user])
