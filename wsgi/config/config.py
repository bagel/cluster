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

    def update(self):
        ctype = "text/plain"
        length = int(self.environ['CONTENT_LENGTH'])
        fileData = json.loads(self.environ['wsgi.input'].read(length))
        collection = self.db[fileData["name"]]
        versionMax = 0
        if collection.count() >= 1:
            versionMax = collection.find(fields={"version": True}, limit=1, sort=[("version", -1)]).next()["version"]
        fileData['mtime'] = int(time.time())
        fileData['version'] = int(versionMax) + 1
        fileData['data'] = fileData['data'].split('@@')
        print collection.insert(fileData)
        return (ctype, "0")

    def delete(self):
        ctype = "text/plain"
        length = int(self.environ['CONTENT_LENGTH'])
        fileData = json.loads(self.environ['wsgi.input'].read(length))
        collection = self.db[fileData["name"]]
        if not fileData.has_key("version"):
            self.db.drop_collection(collection)
        else:
            collection.remove({"version": int(fileData["version"])})
        return (ctype, "0")

    def read(self):
        ctype = "application/json"
        length = int(self.environ['CONTENT_LENGTH'])
        fileData = json.loads(self.environ['wsgi.input'].read(length))
        collection = self.db[fileData["name"]]
        if not fileData.has_key("version"):
            maxData = collection.find(fields={"_id": False}, limit=1, sort=[("version", -1)]).next()
        else:
            maxData = collection.find(spec={"version": int(fileData["version"])}, fields={"_id": False}).next()
        return (ctype, json.JSONEncoder().encode(maxData))

    def history(self):
        ctype = "application/json"
        length = int(self.environ['CONTENT_LENGTH'])
        fileData = json.loads(self.environ['wsgi.input'].read(length))
        collection = self.db[fileData["name"]]
        data = collection.find(fields={"_id": False, "version": True, "author": True, "mtime": True}, sort=[("version", 1)])
        return (ctype, json.JSONEncoder().encode([ d for d in data ]))


class ConfigHtml(ConfigData):
    def __init__(self, environ, template):
        ConfigData.__init__(self, environ, template)

    def response(self):
        ctype = "text/html"
        response_body = script.response(os.path.join(self.template, "config.html"), {})
        return (ctype, response_body)
