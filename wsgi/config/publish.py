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
import paramiko


class Publish:
    def __init__(self):
        self.db = pymongo.MongoClient("10.13.32.21", 2701)["config"]
        self.queue = self.db["queue"]

    def pubHttp(self, cmd, ip):
        sshurl = 'http://dpadmin.grid.sina.com.cn/cgi-bin/ssh.py?'
        data = {"cmd": cmd, "ip": ip}
        return urllib2.urlopen(url = sshurl + urllib.urlencode(data)).read()

    def pubSSH(self, cmd, ip):
        s = paramiko.SSHClient()
        s.load_system_host_keys(filename='/root/.ssh/known_hosts')
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=ip, port=26387, username='root', key_filename='/root/.ssh/id_rsa', timeout=5)
        stdin, stdout, stderr = s.exec_command(cmd)
        return stdout.read() + stderr.read()

    def pub(self):
        for q in self.queue.find(sort=[("version", 1)]):
            print q
            for node in self.db["publish"].find(spec={"version": q["pubversion"]}, fields={"_id": False, "nodes": True}).next()["nodes"]:
                print node
                self.db["issue"].update({"pubversion": q["pubversion"]}, {"$push": { "data": {node.replace('.', '_'): self.pubSSH("/usr/local/bin/manager %s" % q["pubversion"], node)}}})
                self.queue.remove(spec_or_id={"_id": q["_id"]})


def main():
    print Publish().pubSSH("ls", "10.73.48.210")
    Publish().pub()

if __name__ == "__main__":
    main()
