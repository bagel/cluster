#!/usr/bin/env python

import sys
import os
import web

route = {
    "default": ("app/status/high", "High.response"),
    "/status/data": ("app/status/statusMain", "Status.chartData"),
    "/status/sum": ("app/status/statusMain", "Status.sum"),
    "/status/old": ("app/status/statusMain", "Status.response"),
    "/status/high$": ("app/status/high", "High.response"),
    "/status/high/data": ("app/status/high", "High.chartData"),
    "/status/map$": ("app/status/statusMain", "StatusMap.response"),
    "/status/map/data": ("app/status/statusMain", "StatusMap.mapData"),
    "/status/custom/?$": ("app/status/custom", "Custom.response"),
    "/status/custom/domainstatus/?$": ("app/status/custom", "Custom.responseStatus"),
    "/status/custom/domainstatusadd": ("app/status/custom", "Custom.addStatus"),
    "/status/custom/domainstatusdel": ("app/status/custom", "Custom.delStatus"),
}

def urls(environ):
    return web.execute(environ, route)
