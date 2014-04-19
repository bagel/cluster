#!/usr/bin/env python

import sys
import os
import web

route = {
    "default": ("app/status/statusMain", "Status.response"),
    "/status/data": ("app/status/statusMain", "Status.chartData"),
    "/status/node": ("app/status/node", "update"),
    "/status/domain": ("app/status/domain", "update"),
    "/status/sum": ("app/status/statusMain", "Status.sum"),
    "/status/high$": ("app/status/statusMain", "StatusHigh.response"),
    "/status/high/data": ("app/status/statusMain", "statusHigh.chartData"),
    "/status/map$": ("app/status/statusMain", "statusMap.response"),
    "/status/map/data": ("app/status/statusMain", "statusMap.mapData"),
}

def urls(environ):
    template = os.path.join(environ['DOCUMENT_ROOT'], 'app/status/template')
    return web.execute(environ, route, template)
