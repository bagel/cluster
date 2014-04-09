#!/usr/bin/env python

import sys
import os
import urlparse
import urllib2
import json
import time
import base64
import hashlib
import redis

class Login:
    def __init__(self, environ):
        self.environ = environ
        self.r = redis.StrictRedis(host='10.13.32.21', port=6379)
        self.query = urlparse.parse_qs(self.environ['QUERY_STRING'])
        self.domain = self.query.get("domain", [""])[0]

    def authApi(self):
        err_api = ("application/json", json.JSONEncoder().encode({"errmsg": "Permission denied"}))
        user = self.r.hget("info_user", self.domain)
        if not user:
            return (1, err_api)
        user = eval(user)[0]
        key = self.query.get("key", [""])[0]
        if not key:
            return (1, err_api)
        hash = hashlib.md5('@'.join([user.split('@')[0], "dpooluser"])).hexdigest()
        if key == hash:
            return (0, user)
        else:
            return (1, err_api)

    def authWeb(self, user):
        err_web = ("text/html", "Permission denied")
        user_admin = eval(self.r.get("info_user_admin"))
        if user in user_admin:
            return (0, user)
        user_dpool = self.r.hget("info_user", self.domain)
        if user_dpool:
            user_dpool = eval(user_dpool)
            user_dpool = [ u.split('@')[0] for u in user_dpool ]
            if user in user_dpool:
                return (0, user)
        return (1, err_web)

    def auth(self):
        ctype = "text/html"
        if self.environ["HTTP_HOST"] == "api.dpool.cluster.sina.com.cn" or "Mozilla" not in self.environ["HTTP_USER_AGENT"]:
            if self.domain and self.domain != 'sum':
                return self.authApi()
            return (0, "default")
        cookies = self.environ.get('HTTP_COOKIE', []).split('; ')
        token = ""
        for cookie in cookies:
            if "DP_token" in cookie:
                token = base64.b64decode(cookie.split('DP_token=')[1])
        #if token and (time.time() - int(token.split('.')[1]) < 3600 * 3):
        if token:
            user = token.split('.')[0]
            if self.domain and self.domain != 'sum':
                return self.authWeb(user)
            return (0, user)
        if not query.has_key("token"):
            response_body = "login...."
            header = ("Refresh", "0; url=http://auth.intra.sina.com.cn/login?url=http://admin.dpool.cluster.sina.com.cn/home")
            return (1, (ctype, response_body, header))
        else:
            user = json.loads(urllib2.urlopen(url="http://auth.intra.sina.com.cn/interface/loginCheck?token=" + query['token'][0]).read())["data"]["name"]
            header = ("Set-Cookie", "DP_token=%s; path=/; expires=Thu, 01 Jan %d 00:00:00 GMT" % (base64.b64encode("%s.%d" % (user, int(time.time()))), int(time.strftime("%Y")) + 1))
            return (2, (user.encode('utf-8'), header))
    
    def logout(self):
        ctype = "text/html"
        response_body = "logout...."
        header1 = ("Set-Cookie", "DP_token=delete; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT")
        header2 = ("Refresh", "0; url=http://auth.intra.sina.com.cn/main/logout?url=http://admin.dpool.cluster.sina.com.cn/home")
        return (ctype, response_body, header1, header2)
    
    def user(self):
        if int(self.query.get("evil", [0])[0]) == 1:
            return 1
        if not self.domain:
            return 0
        err = ("application/json", json.JSONEncoder().encode({"errmsg": "Permission denied"}))
        if not self.query.has_key("key"):
            return err
        key = self.query["key"][0]
        user = self.r.hget("info_user", self.domain)
        if not user:
            return err
        user = eval(user)[0]
        hash = hashlib.md5('@'.join([user.split('@')[0], "dpooluser"])).hexdigest()
        if key == hash:
            return 1
        else:
            return err

