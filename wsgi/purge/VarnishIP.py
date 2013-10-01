#!/usr/bin/env python

import sys
import os
import json
import urllib2
import threading
import memcache
import time

def checkwb(ip, server):
    url = 'http://w5.lb.sina.com.cn/api/api.php?action=info&realserver='
    try:
        if not json.loads(urllib2.urlopen(url='%s%s' % (url, server['ip_ex'])).readline()) and \
           not json.loads(urllib2.urlopen(url='%s%s' % (url, server['ip_in'])).readline()):
            return 0
        elif server['ip_in'] == "10.55.22.73":
            return 0
        else:
            ip.append(server['ip_in'])
    except:
        return 0

def serverlist():
    url = 'http://dpadmin.grid.sina.com.cn/api/serverlist2.php?mod=varnish'
    ip = []
    threads = []
    for server in json.loads(urllib2.urlopen(url=url).readline())['list']:
        threads.append(threading.Thread(target=checkwb, args=(ip, server)))
        threads[-1].start()
    for t in threads:
        t.join()
    #print len(ip)
    #if ip:
    #    mc = memcache.Client(environ['SINASRV_MEMCACHED_SERVERS'].split(' '))
    #    mc.set('servers', ip, time=time.time()+86400)
        #print len(mc.get('ip'))
    return ip


if __name__ == "__main__":
    environ = {}
    environ['SINASRV_MEMCACHED_SERVERS'] = '10.29.10.227:7601'
    saveip(environ)
