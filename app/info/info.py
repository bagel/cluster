#!/usr/bin/env python

import sys
import os
import script
import redis
import urlparse


class Info:
    def __init__(self, environ, template):
        self.ctype = "text/html"
        self.environ = environ
        self.template = template
        self.query = urlparse.parse_qs(self.environ["QUERY_STRING"])
        self.r=redis.StrictRedis(host='10.13.32.21', port=6379)
        self.node = eval(self.r.get("node"))
        self.idc = eval(self.r.get("idc"))
        self.mod = eval(self.r.get("mod"))
        self.domain = eval(self.r.get("domain"))

    def response(self):
        tdict = {
            "query_string": self.environ["QUERY_STRING"], 
            "qdomain": self.query.get("domain", [""])[0],
            "qip": self.query.get("ip", [""])[0],
            "qidc": self.query.get("idc", [""])[0],
            "qmod": self.query.get("mod", [""])[0],
            "idc": self.idc, 
            "mod": self.mod,
            "domains": list(self.domain)
        }
        return (self.ctype, script.response(os.path.join(self.template, "info.html"), tdict))
