#!/usr/bin/env python

import sys
import os
import web

route = {
    "default": ("app/util/utilMain", "Util.response"),
}

def urls(environ):
    template = os.path.join(environ['DOCUMENT_ROOT'], 'app/util/template')
    return web.execute(environ, route, template)
