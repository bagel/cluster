import sys
import os
import hashlib
import redis
import yaml
import web


def cachefunc(expire=600):
    """Cache function f return value in redis with `expire` time."""
    def _cachefunc(f):
        def __cachefunc(*args, **kwargs):
            r = redis.StrictRedis("10.13.32.21", "6381")
            keys = ["info_func-", f.func_name]
            keys.extend([ '-%s' % arg for arg in args ])
            keys.extend([ '-%s--%s' % (k, v) for k, v in kwargs.iteritems() ])
            key = ''.join(keys)
            print key
            if not r.exists(key):
                print "miss"
                value = f(*args, **kwargs)
                r.setex(key, expire, value)
                return value
            else:
                print "hit"
                value = r.get(key)
                try:
                    return eval(value, {}, {})
                except NameError:
                    return value
        return __cachefunc
    return _cachefunc

@web.cachefunc(expire=86400)
def userkey(user):
    return hashlib.md5('%s@dpooluser' % user).hexdigest()


def localenv(key):
    conf = "/data1/www/htdocs/admin.dpool.cluster.sina.com.cn/conf/main.yaml"
    with open(conf, "r") as fp:
        envs = yaml.load(fp.read())
    for k, v in envs.iteritems():
        if k == key:
            return v
    return None
