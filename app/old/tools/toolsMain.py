#!/usr/bin/env python

import sys
import os
import cgi
import urllib2
import json
import re
import ConfigParser
import subprocess
import urlparse

#sys.path.append('/data1/www/htdocs/api.dpool.cluster.sina.com.cn/libs/')
import augs
import redisdb


class Tools:
    def __init__(self, environ):
        self.environ = environ

    def _request(self, url, data='', headers={}):
        req = urllib2.Request(url=url)
        if data:
            req.add_data(data)
        if headers:
            for key, value in headers.item():
                req.add_header(key, value)
        return urllib2.urlopen(req, timeout=3).read()
    
    def online(self):
        ctype = 'text/plain; charset=utf-8'
        dpurl = 'http://dpadmin.grid.sina.com.cn/api/serverlist2.php?ip='
        wburl = 'http://w5.lb.sina.com.cn/api/api.php?action=info&realserver='
        ip = urlparse.parse_qs(self.environ['QUERY_STRING'])['ip'][0]
        admin = load = desp = port = 0
        dp_data = json.loads(self._request(url=dpurl+ip))
        if not dp_data['list']:
            return (ctype, 'null')
        dp_data = dp_data['list'][0]
        if int(dp_data['status']):
            admin = 1
        if dp_data['desp']:
            desp = 1
        if json.loads(self._request(url=wburl+dp_data['ip_in'])) or \
           json.loads(self._request(url=wburl+dp_data['ip_ex'])):
            load = 1
        try:
            if re.match('OK', self._request(url='http://%s' % ip)):
                port = 1
        except:
            pass
        response_body = json.JSONEncoder().encode({"admin": admin, "load": load, "desp": desp, "port": port})
        #response_body = '%d%d%d%d' % (admin, load, desp, port)
        return (ctype, response_body)
    
    def config(self):
        ctype = 'text/plain; charset=utf-8'
        conf = ConfigParser.ConfigParser()
        conf.read(os.path.join(self.environ['DOCUMENT_ROOT'], 'wsgi/tools/ip.cfg'))
        sec = cgi.parse_qs(self.environ['QUERY_STRING'])['cfg'][0]
        ip = cgi.parse_qs(self.environ['QUERY_STRING'])['ip'][0]
        print ip, sec
        if ip in conf.get(sec, 'ip').strip().split(' '):
            response_body = '1'
        else:
            response_body = '0'
        return (ctype, response_body)
    
    def mail(self):
        ctype = 'text/plain; charset=utf-8'
        sv = "DPool"
        service = "web"
        object = "service"
        length = int(self.environ['CONTENT_LENGTH'])
        data = json.loads(self.environ['wsgi.input'].read(length))
        subject = str(data['subject'])
        content = str(data['content'])
        mailto = str(','.join(data['mailto']))
        p = subprocess.Popen('/etc/dAppCluster/send_alert.pl -sv %s --service %s \
                --object "%s" --subject "%s" --content "%s" --mailto "%s" -html 1' \
                % (sv, service, object, subject, content, mailto), shell=True)
        response_body = str(p.wait())
        return (ctype, response_body)
    
    def publish(self):
        ctype = 'text/plain; charset=utf-8'
        cfg = cgi.parse_qs(self.environ['QUERY_STRING'])['cfg'][0]
        print cfg
        response_body = augs.Role().read(cfg)
        print response_body
        return (ctype, json.JSONEncoder().encode(response_body))
    
    def logset(self):
        ctype = 'text/plain; charset=utf-8'
        print self.environ['QUERY_STRING']
        print "work"
        p = urlparse.parse_qs(urllib2.unquote(self.environ['QUERY_STRING']))
        print p
        k = p['file'][0]
        s = [p['size'][0], p['line'][0], p['dir'][0], p['md5'][0], p['intip'][0], p['role'][0], p['zone'][0], p['time'][0]]
        print s
        print 'work'
        redisdb.Redis().set(k, s)
        return (ctype, '0')
    
    def logget(self):
        ctype = 'application/json'
        file = urlparse.parse_qs(self.environ['QUERY_STRING'])['file'][0]
        response_body = json.JSONEncoder().encode((redisdb.Redis().get(file)))
        return (ctype, response_body)
    
    def logkey(self):
        ctype = 'application/json'
        file = urlparse.parse_qs(self.environ['QUERY_STRING'])['file'][0]
        response_body = json.JSONEncoder().encode((redisdb.Redis().getkey(file)))
        return (ctype, response_body)



if __name__ == "__main__":
    environ = {}
    environ['QUERY_STRING'] = 'zone=tc2&intip=10.73.48.26&role=Web2&file=201305212045-10.72.48.26-80-dpool-apache-www.log.gz&time=2013-05-21+20%3A55%3A12&line=68081&size=8126505&dir=2013-05-21%2F250&md5=5030f669a895907db2554fa25b2f2291'
    logget(environ)
