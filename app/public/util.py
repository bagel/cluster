import sys
import os
import hashlib
import redis


def userkey(user):
    return hashlib.md5('%s@dpooluser' % user).hexdigest()

def cachefunc(f):
    def _cachefunc(*args, **kwargs):
        r = redis.StrictRedis("10.13.32.21", "6381")
        keys = [f.func_name]
        keys.extend([ '-%s' % arg for arg in args ])
        keys.extend([ '-%s--%s' % (k, v) for k, v in kwargs.iteritems() ])
        key = ''.join(keys)
        if not r.hexists('info_func', key):
            value = f(*args, **kwargs)
            r.hset('info_func', key, value)
            return value
        else:
            return r.hget('info_func', key)
    return _cachefunc
