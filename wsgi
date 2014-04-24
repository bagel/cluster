import sys
import os
import web
import app

def application(environ, start_response):
    web.initenv(environ)
    status, response_headers, response_body = app.urls(environ)
    start_response(status, response_headers)
    return [response_body]
