#!/usr/bin/env python

import sys
import os
import config
import re

def urls(environ):
    template = os.path.join(environ['DOCUMENT_ROOT'], 'wsgi/config/template')
    if re.match(r"/config/read", environ['PATH_INFO']):
        return config.ConfigData(environ, template).read()
    elif re.match(r"/config/update", environ['PATH_INFO']):
        return config.ConfigData(environ, template).update()
    elif re.match(r"/config/delete", environ["PATH_INFO"]):
        return config.ConfigData(environ, template).delete()
    elif re.match(r"/config/history", environ["PATH_INFO"]):
        return config.ConfigData(environ, template).history()
    elif re.match(r"/config/node/create", environ["PATH_INFO"]):
        return config.NodeData(environ, template).create()
    elif re.match(r"/config/node/update", environ["PATH_INFO"]):
        return config.NodeData(environ, template).update()
    elif re.match(r"/config/node/add$", environ["PATH_INFO"]):
        return config.NodeData(environ, template).add()
    elif re.match(r"/config/node/read$", environ["PATH_INFO"]):
        return config.NodeData(environ, template).read()
    elif re.match(r"/config/node/history", environ["PATH_INFO"]):
        return config.NodeData(environ, template).history()
    elif re.match(r"/config/node/rename", environ["PATH_INFO"]):
        return config.NodeData(environ, template).rename()
    elif re.match(r"/config/node/addnodes", environ["PATH_INFO"]):
        return config.NodeData(environ, template).addnodes()
    elif re.match(r"/config/node/readnodes", environ["PATH_INFO"]):
        return config.NodeData(environ, template).readnodes()
    elif re.match(r"/config/group/create", environ["PATH_INFO"]):
        return config.ConfigGroup(environ, template).create()
    elif re.match(r"/config/group/add", environ["PATH_INFO"]):
        return config.ConfigGroup(environ, template).add()
    elif re.match(r"/config/group/update", environ["PATH_INFO"]):
        return config.ConfigGroup(environ, template).update()
    elif re.match(r"/config/group/rename", environ["PATH_INFO"]):
        return config.ConfigGroup(environ, template).rename()
    elif re.match(r"/config/group/read", environ["PATH_INFO"]):
        return config.ConfigGroup(environ, template).read()
    elif re.match(r"/config/group/history", environ["PATH_INFO"]):
        return config.ConfigGroup(environ, template).history()
    elif re.match(r"/config/publish/add", environ["PATH_INFO"]):
        return config.ConfigPublish(environ, template).add()
    elif re.match(r"/config/publish/update", environ["PATH_INFO"]):
        return config.ConfigPublish(environ, template).update()
    elif re.match(r"/config/edit$", environ["PATH_INFO"]):
        return config.ConfigHtml(environ, template).configEdit()
    elif re.match(r"/config/edit/post", environ["PATH_INFO"]):
        return config.ConfigHtml(environ, template).configEditPost()
    elif re.match(r"/config/list", environ["PATH_INFO"]):
        return config.ConfigHtml(environ, template).configList()
    elif re.match(r"/config/version", environ["PATH_INFO"]):
        return config.ConfigHtml(environ, template).configVersion()
    elif re.match(r"/config/pub$", environ["PATH_INFO"]):
        return config.ConfigPubHtml(environ, template).configPub()
    elif re.match(r"/config/pub/get", environ["PATH_INFO"]):
        return config.ConfigPubHtml(environ, template).configPubGet()
    elif re.match(r"/config/pub/post", environ["PATH_INFO"]):
        return config.ConfigPubHtml(environ, template).configPubPost()
    elif re.match(r"/config/pub/update", environ["PATH_INFO"]):
        return config.ConfigPubHtml(environ, template).configPubUpdate()
    elif re.match(r"/config/queue/post", environ["PATH_INFO"]):
        return config.ConfigQueue(environ, template).configQueuePost()
    elif re.match(r"/config/issue/post", environ["PATH_INFO"]):
        return config.ConfigIssueHtml(environ, template).configIssuePost()
    elif re.match(r"/config/issue", environ["PATH_INFO"]):
        return config.ConfigIssueHtml(environ, template).configIssue()
    else:
        return config.ConfigPubHtml(environ, template).configPub()
