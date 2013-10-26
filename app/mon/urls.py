#!/usr/bin/env python

import sys
import os
import mon

def urls(environ):
    template = os.path.join(environ['DOCUMENT_ROOT'], 'app/mon/template')
    if environ['PATH_INFO'] == '/mon':
        return mon.Response(environ, template).response()
    else:
        return test.test(environ, template)
