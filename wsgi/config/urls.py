#!/usr/bin/env python

import sys
import os
import config
import re

def urls(environ):
    template = os.path.join(environ['DOCUMENT_ROOT'], 'wsgi/config/template')
    if re.match(r"/status/data", environ['PATH_INFO']):
        return status.Status(environ, template).data()
    elif re.match(r"/status/node", environ['PATH_INFO']):
        import node
        node.update()
        return ("text/plain", "node update ok")
    elif re.match(r"/status/domain", environ["PATH_INFO"]):
        import domain
        domain.update()
        return ("text/plain", "domain update ok")
    else:
        return config.Config(environ, template).response()
