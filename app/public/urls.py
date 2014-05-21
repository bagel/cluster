import sys
import os
import web

route = {
    "default": ("app/public/publicMain", "Home.response"),
    "/login": ("app/public/publicMain", "Login.response"),
    "/profile/?$": ("app/public/profileMain", "Profile.response"),
    "/profile/domainstat/?$": ("app/public/profileMain", "Profile.responseStat"),
    "/profile/domainstatdomain": ("app/public/profileMain", "Profile.responseStatDomain"),
    "/profile/domainauthadd": ("app/public/profileMain", "Profile.domainAuthAdd"),
    "/profile/domainauthdel": ("app/public/profileMain", "Profile.domainAuthDel"),
    "/profile/domainstatus/?$": ("app/public/profileMain", "Profile.responseStatus"),
    "/profile/domainstatusadd": ("app/public/profileMain", "Profile.domainStatusAdd"),
    "/util": ("app/public/publicMain", "Util.response"),
    "^/plot": ("app/public/plot", "Plot.response"),
    "^/online": ("app/public/publicMain", "Online.online"),
    "^/purge": ("app/public/publicMain", "Purge.response"),
    "^/test": ("app/public/testMain", "test"),
    "/convert": ("app/public/convert", "convert"),
    "/env": ("app/public/publicMain", "Public.response_env"),
}

def urls(environ):
    return web.execute(environ, route)
