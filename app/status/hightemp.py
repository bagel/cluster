import sys
import os
import redis
import urlparse
import time
import web
import json
import urllib2
import re



class HighTemp(object):
    def __init__(self, environ):
        self.ctype = "text/html"
        self.environ = environ
        self.query = urlparse.parse_qs(self.environ["QUERY_STRING"])
        self.r = redis.StrictRedis(host=web.getenv("REDIS_STATUS_TEST_HOST"), \
                                   port=int(web.getenv("REDIS_STATUS_TEST_PORT")))
        self.urls = self.query.get("url", [""])
        self.multi = self.query.get("multi", ["0"])[0]

    @web.response
    @web.util.tracefunc
    def response(self):
        self.urls = [ urllib2.unquote(url) for url in self.urls ]
        tdict = {
            "urls": self.urls,
            "multi": self.multi
        }
        return (self.ctype, web.template(self.environ, "hightemp.html", tdict))

