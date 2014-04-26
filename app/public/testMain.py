
import uwsgi
import web
import dpool

uwsgi.cache_set("a", "hello")

@web.timefunc
def test(e):
    print type(dpool.get_serverlist("varnish"))
    #return ("text/html", ":%s:" % "h")
    return web.error.errapi(403)
