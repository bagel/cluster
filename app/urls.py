#!/usr/bin/env python

import sys
import os
import re
import login
import web

route = {
    "default": ("app/public/",),
    "^/config": ("app/config/",),
    "^/status": ("app/status/",),
    "^/mon": ("app/mon/",),
    "^/info": ("app/info/",),
    "^/(home|profile|util|plot|online|purge)": ("app/public/",),
}

def urls(environ):
    environ["TEMP_PATH"] = [os.path.join(environ["DOCUMENT_ROOT"], "app/public/template")]
    environ["USER"] = ""
    path =  environ["PATH_INFO"].split('/')[1]
    if path == "logout":
        return login.Login(environ).logout()
    elif path == "login":
        return login.Login(environ).staffResponse()
    environ = login.Login(environ).auth()
    if not isinstance(environ, dict):
        return environ

    return web.execute(environ, route)
