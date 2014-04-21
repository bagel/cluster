import sys
import os
import urllib2
import json
from util import cachefunc


@cachefunc(expire=3600)
def get_serverlist(mod):
    url = 'http://dpadmin.grid.sina.com.cn/api/serverlist.php?mod=' + mod
    return [ s["ip_in"] for s in json.loads(urllib2.urlopen(url=url).read())["list"] ]

@cachefunc(expire=10, miss=1)
def test():
    return (1, 2)


if __name__ == "__main__":
    #print get_serverlist(mod="varnish")
    print test()
