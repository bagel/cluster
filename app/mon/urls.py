#!/usr/bin/env python

import sys
import os
import web

route = {
    "default": ("app/mon/main", "Mon.response"),
    "/mon/data": ("app/mon/main", "Mon.chartData"),
    "/mon/ws/data": ("app/mon/main", "Mon.wsSubData"),
    "/mon/accesslog": ("app/mon/main", "Mon.LogAccess"),
    "/mon/errorlog": ("app/mon/main", "Mon.LogError"),
    "/mon/accesscount": ("app/mon/main", "Mon.LogAccessCount"),
    "/mon/errorcount": ("app/mon/main", "Mon.LogErrorCount"),
}

def urls(environ):
    template = os.path.join(environ['DOCUMENT_ROOT'], 'app/mon/template')
    return web.execute(environ, route, template)
