#!/usr/bin/env python

import sys
import os
import memcache

#class Memcache:
def connect():
    return memcache.Client(os.environ['SINASRV_MEMCACHED_SERVERS'].split(' '))

def get(key):
    return connect().get(key)

def set(key, val, time=0):
    return connect().set(key, val, time)

def delete(key):
    return connect().delete(key)


if __name__ == '__main__':
    os.environ['MEMCACHE_SERVERS'] = '10.29.10.227:7601'
    if not Memcache().get('test'):
        print 'work'
