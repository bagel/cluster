import sys
import os
import urlparse
import urllib2
import json
import script
import login
import web

class Public(object):
    def __init__(self, environ, template):
        self.environ = environ
        self.template = template


class Home(Public):
    def __init__(self, environ, template):
        super(Home, self).__init__(environ, template)

    def response(self):
        return web.execute(self.environ, ("app/mon/",))


class Util(Public):
    def __init__(self, environ, template):
        super(Util, self).__init__(environ, template)

    def response(self):
        return ("text/html", script.response(os.path.join(self.template, "util.html"), {"user": self.environ["USER"]}))


class Online(Public):
    def __init__(self, environ, template):
        super(Online, self).__init__(environ, template)

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

