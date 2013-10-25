#!/usr/bin/env python

import sys
import os
import pymongo
import redis
import json
import urllib2
import urlparse
import time
import threading
import Queue
import urllib


class Publish:
    def __init__(self):
        self.db = pymongo.MongoClient("10.13.32.21", 2701)["config"]
        self.queue = self.db["queue"]

    def pubHttp(self, cmd, ip):
        sshurl = 'http://dpadmin.grid.sina.com.cn/cgi-bin/ssh.py?'
        data = {"cmd": cmd, "ip": ip}
        return urllib2.urlopen(url = sshurl + urllib.urlencode(data)).read()

    def pub(self):
        for q in self.queue.find(fields={"_id": False}, sort=[("version", 1)]):
            print q
            for node in self.db["publish"].find(spec={"version": q["pubversion"]}, fields={"_id": False, "nodes": True}).next()["nodes"]:
                print node
                print self.pubHttp("/usr/local/bin/manager %s" % q["pubversion"], node)


def main():
    Publish().pub()

if __name__ == "__main__":
    main()
