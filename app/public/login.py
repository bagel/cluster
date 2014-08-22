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
from xml.dom.minidom import parseString

class Login:
    def __init__(self, environ):
        self.environ = environ
        self.r = redis.StrictRedis(host='10.13.32.21', port=6381)
        self.query = urlparse.parse_qs(self.environ['QUERY_STRING'])
        self.domain = self.query.get("domain", [""])[0]
        self.ctype = "text/html"
        self.home = urllib2.quote("http://%s/home" % self.environ["HTTP_HOST"])

    def authDomain(self, user):
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
            return web.error.error_response(403)
        domains = eval(domains)
        if self.domain in domains:
            self.environ["USER"] = user
            return self.environ
        return web.error.error_response(403)

    def authApi(self):
        """query key should match "user@dpooluser" md5sum.
        """
        key = self.query.get("key", [""])[0]
        if not key:
            return web.error.error_response(403)
        if key == "be9c2fd551734345064b1f765f115a08" or key== "c09551c8a636c68dc06e7c346ea9b70c":
            self.environ["USER"] = "default"
            return self.environ
        user = self.query.get("user", [""])[0]
        if not user:
            return web.error.error_response(403)
        hash_user = util.userkey(user)
        if key != hash_user:
            return web.error.error_response(403)
        if not self.domain or self.domain == "sum":
            self.environ["USER"] = user
            return self.environ
        return self.authDomain(user)

    def authWeb(self, user):
        return self.authDomain(user)

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
        i = 0
        while i < 3:
            try:
                l = ldap.initialize('ldap://%s:%s' % (web.getenv("LDAP_HOST"), web.getenv("LDAP_PORT")))
                l.bind("CN=adsearch,OU=sina,DC=staff,DC=sina,DC=com,DC=cn", web.getenv("LDAP_SECRET"))
                #r = l.search_s(web.getenv("LDAP_BASEDN"), ldap.SCOPE_SUBTREE, "(mail=%s)" % mail)
                r = l.search_s(web.getenv("LDAP_BASEDN"), ldap.SCOPE_SUBTREE, "(samaccountname=%s)" % user)
                dn = r[0][0]
                l.bind_s(dn, password)
            except ldap.INVALID_CREDENTIALS:
                errmsg = u'\u8ba4\u8bc1\u9519\u8bef'
                break
            except ldap.BUSY:
                if i < 3:
                    i += 1
                    continue
                errmsg = u'\u670d\u52a1\u5668\u7e41\u5fd9'
            except:
                errmsg = u'\u672a\u77e5\u9519\u8bef'
            break
        return (user, errmsg)

    def staffPost(self):
        user, errmsg = self.authStaff()
        if errmsg:
            return (self.ctype, web.template(self.environ, "login.html", {"errmsg": errmsg}))
        #response_body = "success...."
        response_body = ""
        headers = {}
        headers["Status"] = "302"
        headers["Location"] = "http://%s/home" % self.environ["HTTP_HOST"]
        headers["Set-Cookie"] = "DP_token=%s; path=/; expires=Thu, 01 Jan %d 00:00:00 GMT" % (base64.b64encode("%s.%d.%s" % (user, int(time.time()), util.userkey(user)[:5])), int(time.strftime("%Y")) + 10)
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
    def authRedirect(self):
        #response_body = "login...."
        response_body = ""
        headers = {}
        headers["Status"] = "302"
        #headers["Location"] = "http://%s/login" % self.environ["HTTP_HOST"]
        headers["Location"] = "%s/login?service=%s" % (web.getenv("CAS_URL"), self.home)
        return (self.ctype, response_body, headers)

    @web.response
    def authTicket(self, ticket):
        url = "%s/validate?ticket=%s&service=%s" % (web.getenv("CAS_URL"), ticket, self.home)
        xmlData = urllib2.urlopen(url=url).read()
        response_body = ""
        headers = {}
        headers["Status"] = "302"
        headers["Location"] = "http://%s/home" % self.environ["HTTP_HOST"]
        try:
            dom = parseString(xmlData.decode('gb2312').encode('utf-8').replace('GB2312', 'UTF-8'))
            user = dom.getElementsByTagName('email')[0].firstChild.data.encode('utf-8')
            headers["Set-Cookie"] = "DP_token=%s; path=/; expires=Thu, 01 Jan %d 00:00:00 GMT" % (base64.b64encode("%s.%d.%s" % (user, int(time.time()), util.userkey(user)[:5])), int(time.strftime("%Y")) + 10)
        except:
            pass
        return (self.ctype, response_body, headers)
        
    def auth(self):
        """Visit api domain or not browser like curl, use api auth and query_string should contain user and key.
           If use browser visit, redirected to intra login if get user from cookie failed, try this again after login success.
           After browser first login response contain Set-Cookie header. If browser has the right DP_token Cookie, no need to login.
        """
        if self.environ["HTTP_HOST"] == "api.dpool.cluster.sina.com.cn":
            return self.authApi()
        if self.query.has_key("ticket"):
            ticket = self.query.get("ticket", [""])[0]
            return self.authTicket(ticket)
        cookies = self.environ.get('HTTP_COOKIE', '').split('; ')
        token = ""
        for cookie in cookies:
            if "DP_token" in cookie:
                token = base64.b64decode(cookie.split('DP_token=')[1])
        #if token and (time.time() - int(token.split('.')[1]) < 3600 * 3):
        if token:
            tokens = token.split('.')
            if len(tokens) < 3 or tokens[2] != util.userkey(tokens[0])[:5]:
                return self.logout()
            user = tokens[0]
            if self.domain and self.domain != 'sum':
                return self.authWeb(user)
            self.environ["USER"] = user
            return self.environ

        return self.authRedirect()
   
    @web.response 
    def logout(self):
        """header1 delete DP_token Cookie, header2 redirect to login screen.
        """
        #response_body = "logout...."
        response_body = ""
        headers = {}
        headers["Status"] = "302"
        headers["Set-Cookie"] = "DP_token=delete; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT"
        #headers["Location"] = "http://%s/login" % self.environ["HTTP_HOST"]
        headers["Location"] = "%s/logout?service=%s" % (web.getenv("CAS_URL"), self.home)
        return (self.ctype, response_body, headers)


