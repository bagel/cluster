#!/usr/bin/env python

import sys
import os
import pymongo
import redis
import time
import json
import script
import urlparse


class ConfigData:
    def __init__(self, environ, template):
        self.environ = environ
        self.template = template
        self.db = pymongo.MongoClient("10.13.32.21", 2701)["config"]
        self.data = {}

    def Collection(self):
        if self.environ["REQUEST_METHOD"] == "POST":
            postData = self.environ['wsgi.input'].read(int(self.environ['CONTENT_LENGTH']))
            print postData
            try:
                self.fileData = json.loads(postData)
            except:
                self.fileData = postData
        else:
            self.fileData = self.data
        print self.fileData["name"]
        self.collection = self.db[self.fileData["name"]]

    def update(self):
        ctype = "text/plain"
        self.Collection()
        versionMax = 0
        if self.collection.count() >= 1:
            versionMax = self.collection.find(fields={"version": True}, limit=1, sort=[("version", -1)]).next()["version"]
        self.fileData['mtime'] = int(time.time())
        self.fileData['version'] = int(versionMax) + 1
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


class NodeData(ConfigData):
    def __init__(self, environ, template):
        ConfigData.__init__(self, environ, template)
        self.K = []
        self.V = {}

    def dictSearch(self, d, key, ks=[]):
        for k, v in d.items():
            if k == key:
                ks.append(k)
                self.K = ks[:]
                self.V = v.copy()
            else:
                ks.append(k)
                self.dictSearch(v, key)
                ks.remove(k)

    def test(self):
        d = {"s": {"m": {"p": {}, "q": {}}, "n": {"t": {}}}, "o": {"h": {}}}
        self.dictSearch(d, "m")
        print self.K, self.V

    def create(self):
        ctype = "text/plain"
        self.Collection()
        root = self.fileData["data"]["root"]
        self.fileData["data"] = {root: {}}
        self.fileData["mtime"] = int(time.time())
        self.fileData["version"] = 1
        self.collection.insert(self.fileData)
        return (ctype, "0")

    def add(self):
        ctype = "text/plain"
        self.Collection()
        parent = self.fileData["parent"]
        current = self.fileData["current"]
        node = self.collection.find(fields={"_id": False}, sort=[("version", -1)], limit=1).next()
        node['mtime'] = int(time.time())
        node['version'] = int(node["version"]) + 1
        self.dictSearch(node["data"], parent)
        s = 'node["data"]'
        for key in self.K:
            s += '["' + key + '"]'
        print s
        s += '["%s"]={}' % (current)
        exec(s)
        self.collection.insert(node)
        return (ctype, "0")
 
    def update(self):
        ctype = "text/plain"
        self.Collection()
        delete = self.fileData["delete"]
        node = self.collection.find(fields={"_id": False}, sort=[("version", -1)], limit=1).next()
        node['mtime'] = int(time.time())
        node['version'] = int(node['version']) + 1
        self.dictSearch(node["data"], delete)
        s = 'node["data"]'
        for key in self.K[:-1]:
            s += '["' + key + '"]'
        s += '.pop("%s")' % delete
        exec(s)
        self.collection.insert(node)
        return (ctype, "0")

    def rename(self): 
        ctype = "text/plain"
        self.Collection()
        rename = self.fileData["rename"]
        node = self.collection.find(fields={"_id": False}, sort=[("version", -1)], limit=1).next()
        node['mtime'] = int(time.time())
        node['version'] = int(node['version']) + 1
        self.dictSearch(node["data"], rename[0])
        s = 'node["data"]'
        for key in self.K[:-1]:
            s += '["' + key + '"]'
        exec(s + '.pop("%s")' % rename[0])
        s += '["%s"]=%s' % (rename[1], self.V)
        exec(s)
        self.collection.insert(node)
        return (ctype, "0")

    def addnodes(self):
        ctype = "text/plain"
        self.Collection()
        nodes = self.fileData["nodes"]
        current = self.fileData["current"]
        node = self.collection.find(fields={"_id": False}, sort=[("version", -1)], limit=1).next()
        node['mtime'] = int(time.time())
        node['version'] = int(node['version']) + 1
        self.dictSearch(node["data"], current)
        s = 'node["data"]'
        for key in self.K:
            s += '["' + key + '"]'
        s += '={"nodes": %s}' % nodes
        exec(s)
        self.collection.insert(node)
        return (ctype, "0")

class ConfigGroup(ConfigData):
    def __init__(self, environ, template):
        ConfigData.__init__(self, environ, template)

    def create(self):
        ctype = "text/plain"
        self.Collection()
        self.fileData['mtime'] = int(time.time())
        self.fileData['version'] = 1
        self.fileData["data"] = {}
        print self.fileData
        print self.collection.insert(self.fileData)
        return (ctype, "0")

    def add(self):
        ctype = "text/plain"
        self.Collection()
        group = self.fileData["group"]
        node = self.fileData["node"]
        groupData = self.collection.find(fields={"_id": False}, limit=1, sort=[("version", -1)]).next()
        groupData['mtime'] = int(time.time())
        groupData['version'] = int(groupData["version"]) + 1
        print groupData
        if not groupData["data"].has_key(group):
           groupData["data"][group] = node
        else:
            groupData["data"][group].extend(node)
        self.collection.insert(groupData)
        return (ctype, "0")
   
    def update(self):
        ctype = "text/plain"
        self.Collection()
        group = self.fileData["group"]
        node = self.fileData["node"]
        groupData = self.collection.find(fields={"_id": False}, limit=1, sort=[("version", -1)]).next()
        groupData['mtime'] = int(time.time())
        groupData['version'] = int(groupData["version"]) + 1
        if not node:
            groupData["data"].pop(group)
        else:
            groupData["data"][group].remove(node)
        self.collection.insert(groupData)
        return (ctype, "0")

    def rename(self):
        ctype = "text/plain"
        self.Collection()
        group = self.fileData["group"]
        node = self.fileData["node"]
        groupData = self.collection.find(fields={"_id": False}, limit=1, sort=[("version", -1)]).next()
        groupData['mtime'] = int(time.time())
        groupData['version'] = int(groupData["version"]) + 1
        if not node:
            groupData["data"][group[1]] = groupData["data"][group[0]]
            groupData["data"].pop(group[0])
        else:
            groupData["data"][group].remove(node[0])
            groupData["data"][group].append(node[1])
        self.collection.insert(groupData)
        return (ctype, "0")



class ConfigHtml(ConfigData):
    def __init__(self, environ, template):
        ConfigData.__init__(self, environ, template)

    def configList(self):
        ctype = "text/html"
        conflist = self.db.collection_names(include_system_collections=False)
        for conf in ["node", "group", "groups"]:
            conflist.remove(conf)
        tdict = {}
        for conf in conflist:
            collection = self.db[conf]
            tdict[conf] = collection.find(fields={"_id": False, "name": True, "path": True, "author": True, "mtime": True}, limit=1, sort=[("version", -1)]).next()
            tdict[conf]["mtime"] = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(tdict[conf]["mtime"]))
        response_body = script.response(os.path.join(self.template, "list.html"), tdict)
        return (ctype, response_body)

    def configEdit(self):
        ctype = "text/html"
        self.data = dict(urlparse.parse_qsl(self.environ['QUERY_STRING']))
        tdict = json.loads(self.read()[-1])
        tdict['mtime'] = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(tdict['mtime']))
        response_body = script.response(os.path.join(self.template, "edit.html"), tdict)
        return (ctype, response_body)

    def configEditPost(self):
        ctype = "text/html"
        self.update()
        return (ctype, "0")

    def response(self):
        ctype = "text/html"
        response_body = script.response(os.path.join(self.template, "edit.html"), {})
        return (ctype, response_body)


def main():
    environ = ""
    template = ""
    d = {"s": {"m": {"p": {}, "q": {}}, "n": {"t": {}}}, "o": {"h": {}}}
    NodeData(environ, template).test()

if __name__ == "__main__":
    main()
