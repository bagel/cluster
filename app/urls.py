#!/usr/bin/env python

import sys
import os
import login

route = {
    "default": "default",
    "os": "os",
    "env": "env",
    "config": "config",
    "status": "status",
    "mon": "mon",
    "home": "mon",
    "info": "info",
    "test": "test",
    "purge": "purge",
    "ip": "ip",
    "online": "online",
    "tools": "tools",
    "util": "util",
    "profile": "profile",
}

def urls(environ):
    ctype = "text/plain; charset=utf-8"
    path =  environ["PATH_INFO"].split('/')[1]
    if path == "logout":
        return login.Login(environ).logout()
    check, user = login.Login(environ).auth()
    header = ()
    if check == 0:
        environ["USER"] = user
    elif check == 1:
        return user
    else:
        environ["USER"] = user[0]
        header = user[1]

    if environ["PATH_INFO"] == "/ws" or environ["PATH_INFO"] == "/foobar/":
        import test
        return test.urls(environ)

    if path not in route.keys():
        path = "default"

    if route[path] == "default":
        return (ctype, "It works!")
    elif route[path] == 'env':
        response_body = ''
        for key, value in sorted(environ.items()):
            response_body += "%s => %s\n" % (key, value)
        return (ctype, response_body)
    elif route[path] == 'os':
        response_body = ''
        for key, value in sorted(os.environ.items()):
            response_body += "%s => %s\n" % (key, value)
        return (ctype, response_body)
    elif route[path] == 'online':
        import tools
        return tools.online(environ)
    

    exec('import %s' % route[path])
    if not header:
        return eval('%s.urls(environ)' % route[path])
    else:
        ctype, response_body = eval('%s.urls(environ)' % route[path])
        return (ctype, response_body, header)
