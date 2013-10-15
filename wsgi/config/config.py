#!/usr/bin/env python

import sys
import os
import pymongo
import redis
import time
import json
import script


class ConfigData:
    def __init__(self, environ, template):
        self.environ = environ
        self.template = template
        self.db = pymongo.MongoClient("10.13.32.21", 2701)["config"]

    def Collection(self):
        self.fileData = json.loads(self.environ['wsgi.input'].read(int(self.environ['CONTENT_LENGTH'])))
        self.collection = self.db[self.fileData["name"]]

    def update(self):
        ctype = "text/plain"
        self.Collection()
        versionMax = 0
        if self.collection.count() >= 1:
            versionMax = self.collection.find(fields={"version": True}, limit=1, sort=[("version", -1)]).next()["version"]
        self.fileData['mtime'] = int(time.time())
        self.fileData['version'] = int(versionMax) + 1
        self.fileData['data'] = self.fileData['data'].split('@@')
        print self.collection.insert(self.fileData)
        return (ctype, "0")

    def delete(self):
        ctype = "text/plain"
        self.Collection()
        if not self.fileData.has_key("version"):
            self.db.drop_collection(self.collection)
        else:
            self.collection.remove({"version": int(self.fileData["version"])})
        return (ctype, "0")

    def read(self):
        ctype = "application/json"
        self.Collection()
        if not self.fileData.has_key("version"):
            maxData = self.collection.find(fields={"_id": False}, limit=1, sort=[("version", -1)]).next()
        else:
            maxData = self.collection.find(spec={"version": int(self.fileData["version"])}, fields={"_id": False}).next()
        return (ctype, json.JSONEncoder().encode(maxData))

    def history(self):
        ctype = "application/json"
        self.Collection()
        data = self.collection.find(fields={"_id": False, "version": True, "author": True, "mtime": True}, sort=[("version", 1)])
        return (ctype, json.JSONEncoder().encode([ d for d in data ]))


class ConfigHtml(ConfigData):
    def __init__(self, environ, template):
        ConfigData.__init__(self, environ, template)

    def Collection(self):
        self.fileData = self.data
        self.collection = self.db[self.fileData["name"]]

    def configEdit(self):
        ctype = "text/html"
        self.data = {"name": "nginx.conf"}
        tdict = json.loads(self.read()[-1])
        tdict['mtime'] = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(tdict['mtime']))
        response_body = script.response(os.path.join(self.template, "edit.html"), tdict)
        return (ctype, response_body)

    def response(self):
        ctype = "text/html"
        response_body = script.response(os.path.join(self.template, "edit.html"), {})
        return (ctype, response_body)
