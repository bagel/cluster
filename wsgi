#!/usr/bin/env python

import sys
import os

path = os.path.dirname(os.path.realpath(__file__))
libs = [
    os.path.join(path, 'lib'),
    os.path.join(path, 'app/public'),
    path,
]
[ sys.path.append(lib) for lib in libs if lib not in sys.path ]

def application(environ, start_response):
    import web
    import app
    environ = web.setenv(environ)
    print "env: ", environ
    print sys.path
    status, response_headers, response_body = app.urls(environ)
    start_response(status, response_headers)
    return [response_body]
