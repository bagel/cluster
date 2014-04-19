#!/usr/bin/env python

import sys
import os
import web

route = {
    "^/online": ("app/tools/toolsMain", "Tools.online"),
    "^/plot": ("app/tools/plot", "Plot.response"),
}

def urls(environ):
    return web.execute(environ, route)
