import sys
import os
import urllib2
import json
import web


@web.util.cachefunc(expire=3600)
def get_serverlist(mod):
    url = 'http://dpadmin.grid.sina.com.cn/api/serverlist.php?mod=' + mod
    data = json.loads(urllib2.urlopen(url=url).read())["list"]
    if not data:
        return []
    return [ d["ip_in"].encode('utf-8') for d in data ]

@web.util.cachefunc(expire=3600)
def test():
    return (1, 2)


if __name__ == "__main__":
    print get_serverlist(mod="varnish")
    #print test()
