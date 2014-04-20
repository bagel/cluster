#!/usr/bin/env python

import sys
import os
import redis
import json


class IP:
    def __init__(self, environ):
        self.ctype = "application/json"
        r = redis.StrictRedis("10.13.32.21")
        self.node = eval(r.get("node"))
        self.snat = eval(r.get("snat"))
        self.vip = eval(r.get("vip"))
        self.query = environ['QUERY_STRING']

    def Web(self):
        data = {}
        data["vip"] = self.vip
        data["snat"] = self.snat
        data["node"] = {}
        for k, v in self.node.iteritems():
            if "dpool2_web" not in v.keys() and "dpool3_web" not in v.keys():
                continue
            data["node"][k] = {}
            for m, ips in v.iteritems():
                if m != "dpool2_web" and m != "dpool3_web":
                    continue
                data["node"][k][m] = ips
        return (self.ctype, json.JSONEncoder().encode(data))

    def Web2(self):
        data = {}
        data["vip"] = {}
        for k, v in self.vip.iteritems():
            if "dpool2_web" not in v.keys():
                continue
            data["vip"][k] = v["dpool2_web"]

        data["snat"] = {}
        for k1, v1 in self.snat.iteritems():
            if "dpool2_web" not in v1.keys():
                continue
            data["snat"][k1] = v1["dpool2_web"]

        data["node"] = {}
        for k, v in self.node.iteritems():
            if "dpool2_web" not in v.keys():
                continue
            data["node"][k] = v["dpool2_web"]
        return (self.ctype, json.JSONEncoder().encode(data))

    def Web3(self):
        data = {}
        data["vip"] = {}
        for k, v in self.vip.iteritems():
            if "dpool3_web" not in v.keys():
                continue
            data["vip"][k] = v["dpool3_web"]

        data["snat"] = {}
        for k1, v1 in self.snat.iteritems():
            if "dpool3_web" not in v1.keys():
                continue
            data["snat"][k1] = v1["dpool3_web"]

        data["node"] = {}
        for k, v in self.node.iteritems():
            if "dpool3_web" not in v.keys():
                continue
            data["node"][k] = v["dpool3_web"]
        return (self.ctype, json.JSONEncoder().encode(data))

    def Snat(self):
        snat = []
        for k, v in self.snat.iteritems():
            for k1, v1 in v.iteritems():
                snat.extend(v1)
        return ("text/plain", '\n'.join(snat))

    def response(self):
        if self.query == "web2":
            return self.Web2()
        elif self.query == "web3":
            return self.Web3()
        elif self.query == "snat":
            return self.Snat()
        else:
            return self.Web()


if __name__ == "__main__":
    print IP()
