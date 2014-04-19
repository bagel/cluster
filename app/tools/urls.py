#!/usr/bin/env python

import sys
import os
import web

route = {
    "^/online": ("app/tools/main", "Tools.online"),
    "^/plot": ("app/tools/plot", "Plot.response"),
}

def urls(environ):
    return web.execute(environ, route)
