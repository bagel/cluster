#!/usr/bin/env python

import sys
import os


def urls(environ):
    if environ['PATH_INFO'] == '/ip':
        import ip
        return ip.IPList().Summary(environ)
