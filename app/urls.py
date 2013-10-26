#!/usr/bin/env python

import sys
import os
import re

route = {
    "default": "default",
    "os": "os",
    "env": "env",
    "config": "config",
    "status": "status",
    "mon": "mon",
    "home": "status",
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
    elif environ['PATH_INFO'] == '/os':
        response_body = ''
        for key, value in sorted(os.environ.items()):
            response_body += "%s => %s\n" % (key, value)
        return (ctype, response_body)
    else:
        exec('import %s' % route[path])
        return eval('%s.urls(environ)' % route[path])
