import sys
import os
import urllib2
import json
from util import cachefunc


@cachefunc
def get_serverlist(mod):
    url = 'http://dpadmin.grid.sina.com.cn/api/serverlist.php?mod=' + mod
    return [ s["ip_in"] for s in json.loads(urllib2.urlopen(url=url).read())["list"] ]


if __name__ == "__main__":
    print get_serverlist(mod="varnish")
