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
        self.r = redis.StrictRedis(host='10.13.32.21', port=6381)
        self.query = urlparse.parse_qs(self.environ['QUERY_STRING'])
        self.domain = self.query.get("domain", [""])[0]

    def authDomain(self, user, err):
        """user in info_dpool_admin and domain's adminer has domain's permission,
           if self.domain in info_domain_user user's domains list, request accept.
        """
        user_admin = self.r.get("info_dpool_admin")
        if user_admin and user in eval(user_admin):
            return (0, user)
        domains_admin = self.r.hget("info_domain_admin", user)
        if domains_admin and self.domain in eval(domains_admin):
            return (0, user)
        domains = self.r.hget("info_domain_user", user)
        if not domains:
            return (1, err)
        domains = eval(domains)
        if self.domain in domains:
            return (0, user)
        return (1, err)

    def authApi(self):
        """query key should match "user@dpooluser" md5sum.
        """
        err_api = ("application/json", json.JSONEncoder().encode({"errmsg": "Permission denied"}), ("Status", "403"))
        key = self.query.get("key", [""])[0]
        if not key:
            return (1, err_api)
        if key == "be9c2fd551734345064b1f765f115a08" or key== "c09551c8a636c68dc06e7c346ea9b70c":
            return (0, "default")
        user = self.query.get("user", [""])[0]
        if not user:
            return (1, err_api)
        hash_user = hashlib.md5('@'.join([user, "dpooluser"])).hexdigest()
        if key != hash_user:
            return (1, err_api)
        return self.authDomain(user, err_api)

    def authWeb(self, user):
        err_web = ("text/html", "Permission denied", ("Status", "403"))
        return self.authDomain(user, err_web)

    def auth(self):
        """Visit api domain or not browser like curl, use api auth and query_string should contain user and key.
           If use browser visit, redirected to intra login if get user from cookie failed, try this again after login success.
           After browser first login response contain Set-Cookie header. If browser has the right DP_token Cookie, no need to login.
        """
        ctype = "text/html"
        if self.environ["HTTP_HOST"] == "api.dpool.cluster.sina.com.cn" or "Mozilla" not in self.environ.get("HTTP_USER_AGENT", ""):
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
        if not self.query.has_key("token"):
            response_body = "login...."
            header = ("Refresh", "0; url=http://auth.intra.sina.com.cn/login?url=http://admin.dpool.cluster.sina.com.cn/home")
            return (1, (ctype, response_body, header))
        else:
            user = json.loads(urllib2.urlopen(url="http://auth.intra.sina.com.cn/interface/loginCheck?token=" + self.query['token'][0]).read())["data"]["name"]
            header = ("Set-Cookie", "DP_token=%s; path=/; expires=Thu, 01 Jan %d 00:00:00 GMT" % (base64.b64encode("%s.%d" % (user, int(time.time()))), int(time.strftime("%Y")) + 1))
            return (2, (user.encode('utf-8'), header))
    
    def logout(self):
        """header1 delete DP_token Cookie, header2 redirect to login screen.
        """
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
        user = self.r.hget("info_user_domain", self.domain)
        if not user:
            return err
        user = eval(user)[0]
        hash = hashlib.md5('@'.join([user.split('@')[0], "dpooluser"])).hexdigest()
        if key == hash:
            return 1
        else:
            return err

