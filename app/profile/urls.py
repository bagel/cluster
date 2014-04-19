#!/usr/bin/env python

import sys
import os
import web

route = {
    "default": ("app/profile/main", "Profile.response"),
    "/profile/domainstat": ("app/profile/main", "Profile.responseStat"),
    "/profile/domainstatdomain": ("app/profile/main", "Profile.responseStatDomain"),
    "/profile/domainauthadd": ("app/profile/main", "Profile.domainAuthAdd"),
    "/profile/domainauthdel": ("app/profile/main", "Profile.domainAuthDel"),
}

def urls(environ):
    template = os.path.join(environ['DOCUMENT_ROOT'], 'app/profile/template')
    return web.execute(environ, route, template)
