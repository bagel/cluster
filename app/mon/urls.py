#!/usr/bin/env python

import sys
import os
import time

route = {
    "default": [("mon.Mon",), ("response",)],
    "/mon/data": [("mon.Mon",), ("chartData",)],
    "/mon/ws/data": [("mon.Mon",), ("wsSubData",)],
    "/mon/accesslog": [("mon.Mon",), ("LogAccess",)],
    "/mon/errorlog": [("mon.Mon",), ("LogError",)],
    "/mon/accesscount": [("mon.Mon",), ("LogAccessCount",)],
    "/mon/errorcount": [("mon.Mon",), ("LogErrorCount",)],
}

def urls(environ):
    template = os.path.join(environ['DOCUMENT_ROOT'], 'app/mon/template')
    path =  environ["PATH_INFO"]
    if path not in route.keys():
        path = 'default'
    category = route[path][0][0]
    category_args = "environ, template, " + ", ".join(route[path][0][1:])
    function = route[path][1][0]
    function_args = ", ".join(route[path][1][1:])
    exec('import %s' % category.split('.')[0])
    return eval('%s(%s).%s(%s)' % (category, category_args, function, function_args))
