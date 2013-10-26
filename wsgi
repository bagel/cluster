#!/usr/bin/env python

import sys
import os

env = {
    'REDIS_HOST': '10.13.32.21',
    'REDIS_PORT': '6379',
    'MONGO_HOST': '10.13.32.21',
    'MONGO_PORT': '2701',
    'MEMCACHE_SERVERS': '10.13.32.21:7601',
}
os.environ.update(env)

path = os.path.dirname(os.path.realpath(__file__))
libs = [
    os.path.join(path, 'lib'),
    path,
]
[ sys.path.append(lib) for lib in libs if lib not in sys.path ]


def application(environ, start_response):
    environ.update(os.environ)
    import app
    ctype, response_body = app.urls(environ)

    response_headers = [('Content-Type', ctype), ('Content-Length', str(len(response_body)))]
    status = '200 OK'
    start_response(status, response_headers)
    return [response_body]
