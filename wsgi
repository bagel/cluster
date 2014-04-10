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
    response = app.urls(environ)

    response_headers = [('Content-Type', response[0]), ('Content-Length', str(len(response[1])))]
    [ response_headers.append(response_header) for response_header in response[2:] if response_header ]
    status = '200 OK'
    if len(response_headers) >= 3 and response_headers[2][0] == "Status":
        status = response_headers[2][1]
        response_headers.pop(2)
    start_response(status, response_headers)
    return [response[1]]
