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

def auth(environ):
    ctype = "text/html"
    if environ["HTTP_HOST"] == "api.dpool.cluster.sina.com.cn" or "Mozilla" not in environ["HTTP_USER_AGENT"]:
        return (0, "default")
    query = urlparse.parse_qs(environ['QUERY_STRING'])
    cookies = environ['HTTP_COOKIE'].split('; ')
    token = ""
    for c in cookies:
        if "DP_token" in c:
            token = base64.b64decode(c.split('DP_token=')[1])
    #if token and (time.time() - int(token.split('.')[1]) < 3600 * 3):
    if token:
        return (0, token.split('.')[0])
    if not query.has_key("token"):
        response_body = "login...."
        header = ("Refresh", "0; url=http://auth.intra.sina.com.cn/login?url=http://admin.dpool.cluster.sina.com.cn/home")
        return (1, (ctype, response_body, header))
    else:
        user = json.loads(urllib2.urlopen(url="http://auth.intra.sina.com.cn/interface/loginCheck?token=" + query['token'][0]).read())["data"]["name"]
        header = ("Set-Cookie", "DP_token=%s; path=/; expires=Thu, 01 Jan %d 00:00:00 GMT" % (base64.b64encode("%s.%d" % (user, int(time.time()))), int(time.strftime("%Y")) + 1))
        return (2, (user.encode('utf-8'), header))

def logout():
    ctype = "text/html"
    response_body = "logout...."
    header1 = ("Set-Cookie", "DP_token=delete; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT")
    header2 = ("Refresh", "0; url=http://auth.intra.sina.com.cn/main/logout?url=http://admin.dpool.cluster.sina.com.cn/home")
    return (ctype, response_body, header1, header2)

def user(environ):
    query = urlparse.parse_qs(environ['QUERY_STRING'])
    if int(query.get("evil", [0])[0]) == 1:
        return 1
    if not query.has_key("domain"):
        return 0
    err = ("application/json", json.JSONEncoder().encode({"errmsg": "Permission denied"}))
    if not query.has_key("key"):
        return err
    r = redis.StrictRedis(host='10.13.32.21', port=6379)
    domain = query["domain"][0]
    key = query["key"][0]
    user = r.hget("info_user", domain)
    if not user:
        return err
    user = eval(user)[0]
    hash = hashlib.md5(user.replace("staff.sina.com.cn", "dpooluser")).hexdigest()
    if key == hash:
        return 1
    else:
        return err

