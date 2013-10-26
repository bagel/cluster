#!/usr/bin/env python

import sys
import os
import urllib2
import cgi
import urlparse
import httplib
import socket
import ConfigParser
import VarnishIP
import time
import re
import memcache
import script


def getip(environ, mc):
    cfg = os.path.join(environ['DOCUMENT_ROOT'], 'wsgi/purge/VarnishIP.cfg')
    servers = mc.get('servers')
    if not servers:
        servers = VarnishIP.serverlist()
        mc.set('servers', servers, time=time.time()+86400)
    return servers

def serverlog(environ, host, name, path, head, client, url):
    log = os.path.join(environ['SINASRV_APPLOGS_DIR'], 'server.%s' % time.strftime('%Y%m%d'))
    fp = open(log, 'a+')
    fp.write('%s|%s|%s|%s|%s\n' % (time.strftime('%Y/%m/%d %H:%S:%M'), client, host, head, url))
    fp.close()

def clientlog(environ, client, response):
    log = os.path.join(environ['SINASRV_APPLOGS_DIR'], 'client.%s' % time.strftime('%Y%m%d'))
    fb = open(log, 'a+')
    fb.write('%s|%s|%s' % (time.strftime('%Y/%m/%d %H:%S:%M'), client, response))
    fb.close()
    

def request(environ, host, port, name, path, client, url):
    #conn = httplib.HTTPConnection(host=host, port=port)
    #conn.request(method='PURGE', url=path, headers={"Host": name})
    #res = conn.getresponse()
    conn = socket.socket()
    conn.settimeout(5)
    try:
        conn.connect((host, port))
        conn.send('PURGE %s HTTP/1.1\nHost: %s\n\n' % (path, name))
        head = conn.recv(1024).split('\r\n')[0]
        serverlog(environ, host, name, path, head, client, url)
        if head == 'HTTP/1.1 404 Not in cache.' or head == 'HTTP/1.1 200 Purged.':
            return 0
    except:
        pass
    return 1

def purge(environ):
    ctype = 'text/plain; charset=utf-8'
    response_body = ''
    request_uri = environ['REQUEST_URI']
    if not re.match("/purge\?url=.*", request_uri):
        response_body = script.response(os.path.join(environ['DOCUMENT_ROOT'], 'wsgi/purge/README'), {'host': environ['HTTP_HOST']})
        return (ctype, response_body)
    url = request_uri.split('/purge?url=')[1]
    mc = memcache.Client(environ['SINASRV_MEMCACHED_SERVERS'].split(' '))
    try:
        client = environ['HTTP_X_FORWARDED_FOR']
    except:
        client = environ['REMOTE_ADDR']
    #for url in query['url']:
    if mc.get(url) or mc.get(client):
        print mc.get(client)
        response_body = '%s: Purge too often.\n' % url
        clientlog(environ, client, response_body)
        return (ctype, response_body)
    mc.set(client, 1, time=60)
    name, path = urllib2.splithost('//' + url.split('//')[-1])
    response = {}
    try:
        ip_list = query['ip']
    except:
        ip_list = getip(environ, mc)
    print ip_list
    for ip in ip_list:
        response.update({ip: request(environ, ip, 8899, name, path, client, url)})
    if 1 not in response.values():
        response_body += '%s: Purge OK.\n' % url
        mc.set(url, 1, time=300)
    else:
        response_body += '%s: Purge Failed.\n' % url
    clientlog(environ, client, response_body)
    return (ctype, response_body) 


if __name__ == '__main__':
    environ = {'DOCUMENT_ROOT': '/data1/www/htdocs/c.grid.sina.com.cn'}
    for ip in getip(environ):
        print request(environ, ip , 8899, 'common.jiangsu.sina.com.cn', '/crossdomain.xml')
