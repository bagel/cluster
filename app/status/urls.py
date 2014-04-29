#!/usr/bin/env python

import sys
import os
import web

route = {
    "default": ("app/status/statusMain", "Status.response"),
    "/status/data": ("app/status/statusMain", "Status.chartData"),
    "/status/sum": ("app/status/statusMain", "Status.sum"),
    "/status/high$": ("app/status/high", "High.response"),
    "/status/high/data": ("app/status/high", "High.chartData"),
    "/status/map$": ("app/status/statusMain", "StatusMap.response"),
    "/status/map/data": ("app/status/statusMain", "StatusMap.mapData"),
}

def urls(environ):
    return web.execute(environ, route)
