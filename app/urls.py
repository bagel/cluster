#!/usr/bin/env python

import sys
import os
import re
import login
import web

route = {
    "default": ("app/mon/",),
    "^/config": ("app/config/",),
    "^/status": ("app/status/",),
    "^/mon": ("app/mon/",),
    "^/home": ("app/mon/",),
    "^/info": ("app/info/",),
    "^/purge": ("app/purge/",),
    "^/online": ("app/tools/",),
    "^/util": ("app/util/",),
    "^/profile": ("app/profile/",),
    "^/plot": ("app/tools/",),
}

def urls(environ):
    ctype = "text/plain; charset=utf-8"
    path =  environ["PATH_INFO"].split('/')[1]
    if path == "logout":
        return login.Login(environ).logout()
    elif path == "login" and environ["REQUEST_METHOD"] == "GET":
        return login.Login(environ).loginStaffHtml()
    elif path == "login" and environ["REQUEST_METHOD"] == "POST":
        return login.Login(environ).loginStaffAuth()
    check, res = login.Login(environ).auth()
    if check == 0:
        environ["USER"] = res
    elif check == 1:
        return res

    return web.execute(environ, route)
