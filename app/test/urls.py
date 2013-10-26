#!/usr/bin/env python

import sys
import os
import test


def urls(environ):
    template = os.path.join(environ['DOCUMENT_ROOT'], 'wsgi/test/template')
    if environ['PATH_INFO'] == '/test/vhost':
        return test.vhost(environ, template)
    elif environ['PATH_INFO'] == '/test/post':
        return test.post(environ, template)
    else:
        return test.test(environ, template)
