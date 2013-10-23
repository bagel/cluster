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
        if self.data:
            self.fileData = self.data
        else:
            postData = self.environ['wsgi.input'].read(int(self.environ['CONTENT_LENGTH']))
            print postData
            try:
                self.fileData = json.loads(postData)
            except:
                self.fileData = postData
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
        data = self.collection.find(fields={"_id": False, "version": True, "author": True, "mtime": True}, sort=[("version", -1)])
        return (ctype, json.JSONEncoder().encode([ d for d in data ]))


class NodeData(ConfigData):
    def __init__(self, environ, template):
        ConfigData.__init__(self, environ, template)
        self.K = []
        self.V = {}
        self.N = []

    def dictSearch(self, d, key, ks=[]):
        if isinstance(d, dict):
            for k, v in d.iteritems():
                if k == key:
                    ks.append(k)
                    self.K = ks[:]
                    self.V = v.copy()
                else:
                    ks.append(k)
                    self.dictSearch(v, key, ks)
                    ks.remove(k)

    def test(self):
        d = {"s": {"m": {"p": {}, "q": {}}, "n": {"t": {}}}, "o": {"h": {}}}
        self.dictSearch(d, "o")
        print "K: ", self.K, "V: ", self.V

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
        self.dictSearch(node["data"], parent, [])
        s = 'node["data"]'
        for key in self.K:
            s += '["' + key + '"]'
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
        self.dictSearch(node["data"], delete, [])
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
        self.dictSearch(node["data"], rename[0], [])
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
        self.dictSearch(node["data"], current, [])
        s = 'node["data"]'
        for key in self.K:
            s += '["' + key + '"]'
        s = 'if %s.has_key("nodes"): %s["nodes"].extend(%s)\nelse: %s["nodes"]=%s' % (s, s, nodes, s, nodes)
        #s += '={"nodes": %s}' % nodes
        print s
        exec(s)
        self.collection.insert(node)
        return (ctype, "0")

    def dictNodes(self, d):
        if isinstance(d, dict):
            for k, v in d.iteritems():
                if v.has_key("nodes"):
                    self.N.extend(v["nodes"])
                else:
                    self.dictNodes(d)

    def readnodes(self):
        ctype = "appliction/json"
        if not self.data:
            self.Collection()
            current = self.fileData["current"]
            collection = self.collection
        else:
            current = self.data["current"]
            collection = self.db[self.data["name"]]
        node = collection.find(fields={"_id": False}, sort=[("version", -1)], limit=1).next()
        self.dictSearch(node["data"], current, [])
        self.dictNodes(self.V)
        return (ctype, json.JSONEncoder().encode(self.N))
        

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

class ConfigPublish(NodeData):
    def __init__(self, environ, template):
        NodeData.__init__(self, environ, template)

    def add(self):
        ctype = "text/plain"
        self.Collection()
        versionMax = 0
        if self.collection.count() >= 1:
            versionMax = self.collection.find(fields={"version": True}, limit=1, sort=[("version", -1)]).next()["version"]
        self.fileData['version'] = int(versionMax) + 1
        self.fileData["stime"] = int(time.time())
        self.fileData["confirm"] = 0
        self.fileData["group"] = self.db[self.fileData["file"]].find(fields={"group": True}, limit=1).next()["group"]
        self.data = {"name": "node", "current": self.fileData["group"]}
        self.fileData["nodes"] = json.loads(self.readnodes()[-1])
        if not self.fileData.has_key("fileversion"):
            self.fileData["fileversion"] = self.db[self.fileData["file"]].find(fields={"version": True}, limit=1, sort=[("version", -1)]).next()["version"]
        self.collection.insert(self.fileData)
        return (ctype, "0")

    def update(self):
        ctype = "text/plain"
        self.Collection()
        version = self.fileData["version"]
        self.fileData.pop("name")
        self.fileData.pop("version")
        if self.fileData.has_key("cauthor"):
            self.fileData["ctime"] = int(time.time())
        elif self.fileData.has_key("pauthor"):
            self.fileData["ptime"] = int(time.time())
        self.collection.update({"version": int(version)}, {"$set": self.fileData})
        return (ctype, "0")


class ConfigHtml(ConfigData):
    def __init__(self, environ, template):
        ConfigData.__init__(self, environ, template)

    def configList(self):
        ctype = "text/html"
        conflist = self.db.collection_names(include_system_collections=False)
        tdict = {}
        for conf in conflist:
            collection = self.db[conf]
            if len(collection.find_one()) == 12:
                tdict[conf] = collection.find(fields={"_id": False, "name": True, "path": True, "group": True, "author": True, "mtime": True}, limit=1, sort=[("version", -1)]).next()
                tdict[conf]["mtime"] = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(tdict[conf]["mtime"]))
        response_body = script.response(os.path.join(self.template, "list.html"), tdict)
        return (ctype, response_body)

    def configVersion(self):
        ctype = "text/html"
        self.data = dict(urlparse.parse_qsl(self.environ['QUERY_STRING']))
        response_body = script.response(os.path.join(self.template, "version.html"), {"history": json.loads(self.history()[-1]), "name": self.data["name"]})
        return (ctype, response_body)

    def configEdit(self):
        ctype = "text/html"
        self.data = dict(urlparse.parse_qsl(self.environ['QUERY_STRING']))
        if not self.data.has_key("version"):
            self.data['version'] = self.db["publish"].find(spec={"file":{"$in": [self.data['name']]}}, fields={"_id": False, "fileversion": True}, limit=1, sort=[("version", -1)]).next()["fileversion"]
        if self.data["name"] != "add":
            tdict = json.loads(self.read()[-1])
            tdict['mtime'] = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(tdict['mtime']))
        else:
            tdict = {"name": "", "path": "", "owner": "", "perm": "", "group": "", "cmd0": "", "cmd1": "", "data": "", "author": "", "mtime": ""}
        if self.db["publish"].find(spec={"$and": [{"file":{"$in": [tdict['name']]}}, {"confirm":{"$in": [0, 1]}}]}).count() >= 1:
            disabled = "disabled"
        else:
            disabled = ""
        tdict["disabled"] = disabled
        response_body = script.response(os.path.join(self.template, "edit.html"), tdict)
        return (ctype, response_body)

    def configEditPost(self):
        self.update()


class ConfigPubHtml(ConfigPublish):
    def __init__(self, environ, template):
        ConfigPublish.__init__(self, environ, template)

    def configPub(self):
        ctype = "text/html"
        if self.environ["REQUEST_METHOD"] == "GET":
            query_string = urlparse.parse_qs(self.environ["QUERY_STRING"])
            if not query_string.has_key("page"):
                self.data = {"name": "publish", "page": 1}
            else:
                self.data = {"name": "publish", "page": int(query_string["page"][0])}
        self.Collection()
        page = int(self.fileData["page"])
        count = self.collection.count()
        if count % 12 == 0:
            pageMax = count / 12
        else:
            pageMax = count / 12 + 1
        pubData = [ d for d in self.collection.find(fields={"_id": False}, sort=[("stime", -1)]) ]
        pubData = pubData[((page - 1) * 12):(page * 12)]
        response_body = script.response(os.path.join(self.template, "publish.html"), {"pubData": pubData, "page": page, "pageMax": pageMax})
        return (ctype, response_body)

    def configPubGet(self):
        ctype = "text/html"
        self.data = dict(urlparse.parse_qsl(self.environ['QUERY_STRING']))
        self.data['file'] = self.data['name']
        self.data['name'] = 'publish'
        self.data['sauthor'] = 'caoyu2'
        self.add()
        return self.configPub()

    def configPubPost(self):
        self.add()

    def configPubUpdate(self):
        self.update()

class ConfigQueue(ConfigData):
    def __init__(self, environ, template):
        ConfigData.__init__(self, environ, template)

    def configQueuePost(self):
        self.update()



def main():
    environ = ""
    template = ""
    d = {"s": {"m": {"p": {}, "q": {}}, "n": {"t": {}}}, "o": {"h": {}}}
    NodeData(environ, template).test()

if __name__ == "__main__":
    main()
