#!/usr/bin/env python

import sys
import os
import test
import publish


def urls(environ):
    template = os.path.join(environ['DOCUMENT_ROOT'], 'wsgi/vhost/template')
    if environ['PATH_INFO'] == '/vhost':
        if environ['REQUEST_METHOD'] == 'POST':
            return publish.post(environ, template)
        return publish.edit(environ, template)
    elif environ['PATH_INFO'] == '/vhost/pub':
        return publish.pub(environ)
    else:
        return test.test(environ, template)
