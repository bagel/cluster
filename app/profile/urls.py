#!/usr/bin/env python

import sys
import os
import web

route = {
    "default": ("app/profile/profileMain", "Profile.response"),
    "/profile/domainstat": ("app/profile/profileMain", "Profile.responseStat"),
    "/profile/domainstatdomain": ("app/profile/profileMain", "Profile.responseStatDomain"),
    "/profile/domainauthadd": ("app/profile/profileMain", "Profile.domainAuthAdd"),
    "/profile/domainauthdel": ("app/profile/profileMain", "Profile.domainAuthDel"),
}

def urls(environ):
    template = os.path.join(environ['DOCUMENT_ROOT'], 'app/profile/template')
    return web.execute(environ, route, template)
