#!/usr/bin/env python

import sys
import os
import urllib2
import re

def domainConf(conf):
    url = 'http://dpadmin.grid.sina.com.cn/api/fetch_newestfile.php?title=' + conf
    return urllib2.urlopen(url).readlines()

def domainWeb2():
    d = []
    for line in domainConf('web2_httpd_vhost.conf'):
        if re.match(r'\s*(ServerName|ServerAlias)', line):
            d.append(line.strip().split(' ')[-1].strip('@@'))
    return d

def domainWeb3():
    d = []
    for line in domainConf('nginx.conf.vhost_fpm'):
        if re.match(r'\s+server_name', line):
            #if "var=get_servername" in line:
            #    d.extend([ m for m in re.sub(r'\s+server_name\s+\[\-.*\-\]\s+(.*)\s*;', r'\1', line).rstrip(';').strip().split(' ') if m ])
            d.extend([ m for m in re.sub(r'\s+server_name\s+@@.*@@\s+(.*)\s*;', r'\1', line).rstrip(';').strip().split(' ') if m ])
    return d

def update(e, t):
    import redis
    r = redis.StrictRedis("10.13.32.21")
    d = set()
    dm = domainWeb2() + domainWeb3()
    for m in dm:
        d.add(m)
    r.set("domain", d)
    return ("text/html", "domain update ok")


if __name__ == "__main__":
    #print len(domainWeb2())
    update()
