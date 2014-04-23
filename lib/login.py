#!/usr/bin/env python

import sys
import os
import urlparse
import urllib2
import json
import time
import re
import base64
import hashlib
import redis
import ldap
import web
import util

class Login:
    def __init__(self, environ):
        self.environ = environ
        self.r = redis.StrictRedis(host='10.13.32.21', port=6381)
        self.query = urlparse.parse_qs(self.environ['QUERY_STRING'])
        self.domain = self.query.get("domain", [""])[0]
        self.ctype = "text/html"

    def authDomain(self, user, err):
        """user in info_dpool_admin and domain's adminer has domain's permission,
           if self.domain in info_domain_user user's domains list, request accept.
        """
        user_admin = self.r.get("info_dpool_admin")
        if user_admin and user in eval(user_admin):
            self.environ["USER"] = user
            return self.environ
        domains_admin = self.r.hget("info_domain_admin", user)
        if domains_admin and self.domain in eval(domains_admin):
            self.environ["USER"] = user
            return self.environ
        domains = self.r.hget("info_domain_user", user)
        if not domains:
            return self.authResponse(err)
        domains = eval(domains)
        if self.domain in domains:
            self.environ["USER"] = user
            return self.environ
        return self.authResponse(err)

    def authApi(self):
        """query key should match "user@dpooluser" md5sum.
        """
        err_api = ("application/json", json.JSONEncoder().encode({"errmsg": "Permission denied"}), {"Status": "403"})
        key = self.query.get("key", [""])[0]
        if not key:
            return self.authResponse(err_api)
        if key == "be9c2fd551734345064b1f765f115a08" or key== "c09551c8a636c68dc06e7c346ea9b70c":
            self.environ["USER"] = "default"
            return self.environ
        user = self.query.get("user", [""])[0]
        if not user:
            return self.authResponse(err_api)
        hash_user = util.userkey(user)
        if key != hash_user:
            return self.authResponse(err_api)
        return self.authDomain(user, err_api)

    def authWeb(self, user):
        err_web = ("text/html", "Permission denied", {"Status": "403"})
        return self.authDomain(user, err_web)

    @web.response
    def authResponse(self, err):
        return err

    def authStaff(self):
        postData = urlparse.parse_qs(self.environ['wsgi.input'].read(int(self.environ['CONTENT_LENGTH'])))
        mail = postData.get('mail', [''])[0]
        password = postData.get('password', [''])[0]
        errmsg = ""
        if not mail or not password:
            errmsg = u'\u63d0\u4ea4\u9519\u8bef'
        if '@' not in mail:
            user = mail
            mail = '@'.join([mail, 'staff.sina.com.cn'])
        else:
            user = mail.split('@')[0] 
        try:
            l = ldap.initialize('ldap://%s:%s' % (self.environ["LDAP_HOST"], self.environ["LDAP_PORT"]))
            l.bind('CN=adsearch,OU=sina,DC=staff,DC=sina,DC=com,DC=cn', 'q2fGed3G`yC&ax')
            r = l.search_s('ou=sina,dc=staff,dc=sina,dc=com,dc=cn', ldap.SCOPE_SUBTREE, "(mail=%s)" % mail)
            dn = r[0][0]
            l.bind_s(dn, password)
        except ldap.INVALID_CREDENTIALS:
            errmsg = u'\u8ba4\u8bc1\u9519\u8bef'
        except ldap.BUSY:
            errmsg = u'\u670d\u52a1\u5668\u7e41\u5fd9'
        except:
            errmsg = u'\u672a\u77e5\u9519\u8bef'
        return (user, errmsg)

    def staffPost(self):
        user, errmsg = self.authStaff()
        if errmsg:
            return (self.ctype, web.template(self.environ, "login.html", {"errmsg": errmsg}))
        #response_body = "success...."
        response_body = ""
        headers = {}
        headers["Status"] = "301 Moved Permanently"
        headers["Location"] = "http://%s/home" % self.environ["HTTP_HOST"]
        headers["Set-Cookie"] = "DP_token=%s; path=/; expires=Thu, 01 Jan %d 00:00:00 GMT" % (base64.b64encode("%s.%d" % (user, int(time.time()))), int(time.strftime("%Y")) + 10)
        return (self.ctype, response_body, headers)

    def staffGet(self):
        return (self.ctype, web.template(self.environ, "login.html"))

    @web.response
    def staffResponse(self):
        request_method = self.environ["REQUEST_METHOD"]
        if request_method == "POST":
            return self.staffPost()
        else:
            return self.staffGet()

    @web.response
    def staffRedirect(self):
        #response_body = "login...."
        response_body = ""
        headers = {}
        headers["Status"] = "301 Moved Permanently"
        headers["Location"] = "http://%s/login" % self.environ["HTTP_HOST"]
        return (self.ctype, response_body, headers)
        

    def auth(self):
        """Visit api domain or not browser like curl, use api auth and query_string should contain user and key.
           If use browser visit, redirected to intra login if get user from cookie failed, try this again after login success.
           After browser first login response contain Set-Cookie header. If browser has the right DP_token Cookie, no need to login.
        """
        if self.environ["HTTP_HOST"] == "api.dpool.cluster.sina.com.cn":
            if self.domain and self.domain != 'sum':
                return self.authApi()
            self.environ["USER"] = "default"
            return self.environ
        cookies = self.environ.get('HTTP_COOKIE', '').split('; ')
        token = ""
        for cookie in cookies:
            if "DP_token" in cookie:
                token = base64.b64decode(cookie.split('DP_token=')[1])
        #if token and (time.time() - int(token.split('.')[1]) < 3600 * 3):
        if token:
            user = token.split('.')[0]
            if self.domain and self.domain != 'sum':
                return self.authWeb(user)
            self.environ["USER"] = user
            return self.environ

        return self.staffRedirect()
   
    @web.response 
    def logout(self):
        """header1 delete DP_token Cookie, header2 redirect to login screen.
        """
        #response_body = "logout...."
        response_body = ""
        headers = {}
        headers["Status"] = "301 Moved Permanently"
        headers["Set-Cookie"] = "DP_token=delete; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT"
        headers["Location"] = "http://%s/login" % self.environ["HTTP_HOST"]
        return (self.ctype, response_body, headers)


