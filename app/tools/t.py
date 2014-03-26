#!/usr/bin/env python

import sys
import os
import json
import urllib2

def pic():
    req = urllib2.Request(url="http://test.dpool.cluster.sina.com.cn/tools/plot")
    data = {
        "y": [{
            "data": range(10000),
            "label": "range",
        }],
    }
    req.add_data(json.JSONEncoder().encode(data))
    return urllib2.urlopen(req).read()


if __name__ == "__main__":
    print pic()
