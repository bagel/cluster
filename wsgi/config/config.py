#!/usr/bin/env python

import sys
import os
import pymongo
import redis
import time


class Config:
    def __init__(self, environ, template):
        self.environ = environ
        self.template = template

    def add(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def response(self):
        ctype = "text/html"
        return (ctype, "config")
