#!/usr/bin/env python

import sys
import os
import json
import redis


class Redis:
    def connect(self):
        #redis_host = '127.0.0.1'
        #redis_port =  6379
        host = os.environ['REDIS_HOST']
        port = os.environ['REDIS_PORT']
        return redis.StrictRedis(host=host, port=int(port))
    
    def set(self, key, values):
        r = self.connect()
        for v in values:
            r.rpush(key, v)

    def get(self, key):
        r = self.connect()
        keys = r.keys(key + '*')
        res = []
        for k in keys:
            t = r.lrange(k, 0, -1)
            t.insert(0, k)
            res.append(t)
        return res

    def getkey(self, pattern):
        r = self.connect()
        return sorted(r.keys(pattern + '*'))


if __name__ == "__main__":
    print Redis().getkey('2')
