#!/usr/bin/env python

import sys
import os
import time

route = {
    "default": [("info.Info",), ("response",)],
    "/info/data": [("info.InfoData",), ("response",)],
}

def urls(environ):
    template = os.path.join(environ['DOCUMENT_ROOT'], 'app/info/template')
    path =  environ["PATH_INFO"]
    if path not in route.keys():
        path = 'default'
    category = route[path][0][0]
    category_args = "environ, template, " + ", ".join(route[path][0][1:])
    function = route[path][1][0]
    function_args = ", ".join(route[path][1][1:])
    exec('import %s' % category.split('.')[0])
    return eval('%s(%s).%s(%s)' % (category, category_args, function, function_args))
