#!/usr/bin/env python

import sys
import os
import web

route = {
    "default": ("app/mon/monMain", "Mon.response"),
    "/mon/data": ("app/mon/monMain", "Mon.chartData"),
    "/mon/ws/data": ("app/mon/monMain", "Mon.wsSubData"),
    "/mon/accesslog": ("app/mon/monMain", "Mon.LogAccess"),
    "/mon/errorlog": ("app/mon/monMain", "Mon.LogError"),
    "/mon/accesscount": ("app/mon/monMain", "Mon.LogAccessCount"),
    "/mon/errorcount": ("app/mon/monMain", "Mon.LogErrorCount"),
    "/mon/charts": ("app/mon/monMain", "Mon.responseTemp"),
}

def urls(environ):
    return web.execute(environ, route)
