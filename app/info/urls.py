#!/usr/bin/env python

import sys
import os
import web

route = {
    "default": ("app/info/infoMain", "Info.response"),
    "/info/data": ("app/info/infoMain", "InfoData.response"),
}

def urls(environ):
    return web.execute(environ, route)
