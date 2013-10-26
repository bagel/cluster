#!/usr/bin/env python

import sys
import os

route = {
    "default": "default",
    "os": "os",
    "env": "env",
    "config": "config",
    "status": "status",
    "mon": "mon",
    "home": "status",
    "info": "info",
    "test": "test",
    "purge": "purge",
    "ip": "ip",
    "online": "online",
}

def urls(environ):
    ctype = "text/plain; charset=utf-8"
    path =  environ["PATH_INFO"].split('/')[1]
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
    return eval('%s.urls(environ)' % route[path])
