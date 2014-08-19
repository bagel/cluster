import sys
import os
import redis
import urlparse
import time
import web
import json



class HighTemp(object):
    def __init__(self, environ):
        self.ctype = "text/html"
        self.environ = environ
        self.query = urlparse.parse_qs(self.environ["QUERY_STRING"])
        self.r = redis.StrictRedis(host=web.getenv("REDIS_STATUS_TEST_HOST"), \
                                   port=int(web.getenv("REDIS_STATUS_TEST_PORT")))
        self.qurl = self.query.get("url", [""])[0]

    @web.response
    @web.util.tracefunc
    def response(self):
        return (self.ctype, web.template(self.environ, "hightemp.html", {"qurl": self.qurl}))

