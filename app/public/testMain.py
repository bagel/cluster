import sys
import os
import uwsgi
import web
import dpool


@web.response
@web.util.timefunc
@web.util.logfunc
@web.util.logfunc
def test(e):
    web.setenv("test", "hello")
    web.setenv("test", "world")
    web.delenv("test")
    print os.environ["HTTP_HOST"]
    print >>sys.stderr,"test error"
    return ("text/html", ":%s:" % os.environ["HTTP_HOST"])
