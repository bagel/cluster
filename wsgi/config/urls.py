#!/usr/bin/env python

import sys
import os

route = {
    "default": [("config.ConfigPubHtml",), ("configPub",)],
    "/config/read": [("config.ConfigData",), ("read",)],
    "/config/update": [("config.ConfigData",), ("update",)],
    "/config/delete": [("config.ConfigData",), ("delete",)],
    "/config/history": [("config.ConfigData",), ("history",)],
    "/config/node/create": [("config.NodeData",), ("create",)],
    "/config/node/update": [("config.NodeData",), ("update",)],
    "/config/node/add": [("config.NodeData",), ("add",)],
    "/config/node/read": [("config.NodeData",), ("read",)],
    "/config/node/history": [("config.NodeData",), ("history",)],
    "/config/node/rename": [("config.NodeData",), ("rename",)],
    "/config/node/addnodes": [("config.NodeData",), ("addnodes",)],
    "/config/node/readnodes": [("config.NodeData",), ("readnodes",)],
    "/config/group/create": [("config.ConfigGroup",), ("create",)],
    "/config/group/add": [("config.ConfigGroup",), ("add",)],
    "/config/group/update": [("config.ConfigGroup",), ("update",)],
    "/config/group/rename": [("config.ConfigGroup",), ("rename",)],
    "/config/group/read": [("config.ConfigGroup",), ("read",)],
    "/config/group/history": [("config.ConfigGroup",), ("history",)],
    "/config/publish/add": [("config.ConfigGroup",), ("add",)],
    "/config/publish/update": [("config.ConfigGroup",), ("update",)],
    "/config/edit": [("config.ConfigHtml",), ("configEdit",)],
    "/config/edit/post": [("config.ConfigHtml",), ("configEditPost",)],
    "/config/list": [("config.ConfigHtml",), ("configList",)],
    "/config/version": [("config.ConfigHtml",), ("configVersion",)],
    "/config/pub": [("config.ConfigPubHtml",), ("configPub",)],
    "/config/pub/get": [("config.ConfigPubHtml",), ("configPubGet",)],
    "/config/pub/post": [("config.ConfigPubHtml",), ("configPubPost",)],
    "/config/pub/update": [("config.ConfigPubHtml",), ("configPubUpdate",)],
    "/config/queue/post": [("config.ConfigQueue",), ("configQueuePost",)],
    "/config/issue/post": [("config.ConfigIssueHtml",), ("configIssuePost",)],
    "/config/issue": [("config.ConfigIssueHtml",), ("configIssue",)],
}

def urls(environ):
    template = os.path.join(environ['DOCUMENT_ROOT'], 'wsgi/config/template')
    path =  environ["PATH_INFO"]
    if path not in route.keys():
        path = 'default'
    category = route[path][0][0]
    category_args = "environ, template, " + ", ".join(route[path][0][1:])
    function = route[path][1][0]
    function_args = ", ".join(route[path][1][1:])
    exec('import %s' % category.split('.')[0])
    return eval('%s(%s).%s(%s)' % (category, category_args, function, function_args))
