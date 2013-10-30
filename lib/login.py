#!/usr/bin/env python

import sys
import os
import urlparse
import urllib2
import json
import time
import base64

def auth(environ):
    ctype = "text/html"
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
        header = ("Refresh", "0; url=http://auth.intra.sina.com.cn/login?url=http://api.dpool.cluster.sina.com.cn/home")
        return (1, (ctype, response_body, header))
    else:
        user = json.loads(urllib2.urlopen(url="http://auth.intra.sina.com.cn/interface/loginCheck?token=" + query['token'][0]).read())["data"]["name"]
        header = ("Set-Cookie", "DP_token=%s" % base64.b64encode("caoyu2.%d" % int(time.time())))
        return (2, (user.encode('utf-8'), header))

def logout():
    ctype = "text/html"
    response_body = "logout...."
    header1 = ("Set-Cookie", "DP_token=delete; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT")
    header2 = ("Refresh", "0; url=http://auth.intra.sina.com.cn/main/logout?url=http://api.dpool.cluster.sina.com.cn/home")
    return (ctype, response_body, header1, header2)
