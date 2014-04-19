#!/usr/bin/env python

import sys
import os
import web

route = {
    "default": ("app/info/infoMain", "Info.response"),
    "/info/data": ("app/info/infoMain", "InfoData.response"),
}

def urls(environ):
    template = os.path.join(environ['DOCUMENT_ROOT'], 'app/info/template')
    return web.execute(environ, route, template)
