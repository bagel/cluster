#!/usr/bin/env python

import sys
import os
import status
import re

def urls(environ):
    template = os.path.join(environ['DOCUMENT_ROOT'], 'app/status/template')
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
    elif re.match(r"/status/sum", environ['PATH_INFO']):
        return status.Status(environ, template).sum()
    elif re.match(r"/status/high$", environ['PATH_INFO']):
        return status.StatusHigh(environ, template).response()
    elif re.match(r"/status/high/data", environ['PATH_INFO']):
        return status.StatusHigh(environ, template).data()
    else:
        return status.Status(environ, template).response()
