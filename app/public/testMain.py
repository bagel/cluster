import sys
import os
import uwsgi
import web
import dpool
import cPickle


@web.response
@web.util.timefunc
@web.util.tracefunc
def test(e):
    print web.getenv("TEMP_PATH")
    return ("text/html", ":%s:" % "test")
