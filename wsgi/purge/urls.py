#!/usr/bin/env python

import purge

def urls(environ):
    if environ['PATH_INFO'][:6] == '/purge':
        return purge.purge(environ)
