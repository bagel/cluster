#!/usr/bin/env python

import sys
import os
import web

route = {
    "default": ("app/config/configMain", "ConfigPubHtml.configPub"),
    "/config/read": ("app/config/configMain", "ConfigData.read"),
    "/config/update": ("app/config/configMain", "ConfigData.update"),
    "/config/delete": ("app/config/configMain", "ConfigData.delete"),
    "/config/history": ("app/config/configMain", "ConfigData.history"),
    "/config/node/create": ("app/config/configMain", "NodeData.create"),
    "/config/node/update": ("app/config/configMain", "NodeData.update"),
    "/config/node/add": ("app/config/configMain", "NodeData.add"),
    "/config/node/read": ("app/config/configMain", "NodeData.read"),
    "/config/node/history": ("app/config/configMain", "NodeData.history"),
    "/config/node/rename": ("app/config/configMain", "NodeData.rename"),
    "/config/node/addnodes": ("app/config/configMain", "NodeData.addnodes"),
    "/config/node/readnodes": ("app/config/configMain", "NodeData.readnodes"),
    "/config/node/deletenodes": ("app/config/configMain", "NodeData.deletenodes"),
    "/config/group/create": ("app/config/configMain", "ConfigGroup.create"),
    "/config/group/add": ("app/config/configMain", "ConfigGroup.add"),
    "/config/group/update": ("app/config/configMain", "ConfigGroup.update"),
    "/config/group/rename": ("app/config/configMain", "ConfigGroup.rename"),
    "/config/group/read": ("app/config/configMain", "ConfigGroup.read"),
    "/config/group/history": ("app/config/configMain", "ConfigGroup.history"),
    "/config/publish/add": ("app/config/configMain", "ConfigGroup.add"),
    "/config/publish/update": ("app/config/configMain", "ConfigGroup.update"),
    "/config/edit": ("app/config/configMain", "ConfigHtml.configEdit"),
    "/config/edit/post": ("app/config/configMain", "ConfigHtml.configEditPost"),
    "/config/list": ("app/config/configMain", "ConfigHtml.configList"),
    "/config/version": ("app/config/configMain", "ConfigHtml.configVersion"),
    "/config/pub": ("app/config/configMain", "ConfigPubHtml.configPub"),
    "/config/pub/get": ("app/config/configMain", "ConfigPubHtml.configPubGet"),
    "/config/pub/post": ("app/config/configMain", "ConfigPubHtml.configPubPost"),
    "/config/pub/update": ("app/config/configMain", "ConfigPubHtml.configPubUpdate"),
    "/config/queue/post": ("app/config/configMain", "ConfigQueue.configQueuePost"),
    "/config/issue/post": ("app/config/configMain", "ConfigIssueHtml.configIssuePost"),
    "/config/issue": ("app/config/configMain", "ConfigIssueHtml.configIssue"),
    "/config/node": ("app/config/configMain", "ConfigNodeHtml.configNode"),
}

def urls(environ):
    template = os.path.join(environ['DOCUMENT_ROOT'], 'app/config/template')
    return web.execute(environ, route, template)
