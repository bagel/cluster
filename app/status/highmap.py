import sys
import os
import redis
import time
import json
import urlparse
import web

class HighMap(object):
    def __init__(self, environ):
        self.environ = environ
        self.ctype = "text/html"
        self.r = redis.StrictRedis(host=web.getenv("REDIS_MAP_HOST"), \
                                   port=int(web.getenv("REDIS_MAP_PORT")))
        self.query = urlparse.parse_qs(self.environ["QUERY_STRING"])
        self.qdomain = self.query.get("domain", ["sum"])[0]

    @web.response
    def mapData(self):
        yday = time.strftime("%Y%m%d", time.localtime(time.time() - 86400))
        print yday
        mapdata = eval(self.r.hget("map%s" % yday, self.qdomain))
        return ("application/json", json.dumps(mapdata))

    @web.response
    def response(self):
        tdict = {
            "query_string": self.environ["QUERY_STRING"],
            "qdomain": self.qdomain,
        }
        return (self.ctype, web.template(self.environ, "highmap.html", tdict))
