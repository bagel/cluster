#!/usr/bin/env python

import sys
import os
import redis
import urllib2
import json
import util2 as util


def domainCmdb(domain):
    url = "http://newcmdb.intra.sina.com.cn/api?username=api4cli&auth=jBv5N1hVw1Z3dpASG507W18B&q=domain_name=="
    req = urllib2.Request(url = url + domain)
    req.add_header("accept", "application/json")
    return json.loads(urllib2.urlopen(req).read())['result']

def domainUserSet():
    r = redis.StrictRedis(util.localenv("REDIS_INFO_HOST"), util.localenv("REDIS_INFO_PORT"))
    domains = eval(r.get('info_domain'))
    domain_admin = {}
    for domain in domains:
        cmdb = domainCmdb(domain)
        if not cmdb:
            continue
        admin0 = cmdb[0]['dns_admin0']
        if not domain_admin.has_key(admin0):
            domain_admin[admin0] = []
        domain_admin[admin0].append(domain)
        print domain_admin
    r.hmset("info_domain_admin", domain_admin)


if __name__ == "__main__":
    domainUserSet()
