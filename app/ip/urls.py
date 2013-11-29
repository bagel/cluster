#!/usr/bin/env python

import sys
import os
import ip


def urls(environ):
    if environ['PATH_INFO'] == '/ip':
        return ip.IP(environ).response()
