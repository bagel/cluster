
import uwsgi
import web
import dpool


@web.response
@web.util.timefunc
def test(e):
    web.setenv("test", "hello")
    web.setenv("test", "world")
    return ("text/html", ":%s:" % web.getenv("test"))
