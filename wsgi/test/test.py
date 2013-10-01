#!/usr/bine/env python

import sys
import os
import script
import augs


def test(environ, template):
    ctype = 'text/html'
    tdict = {'t': 'test'}
    response_body = script.response(os.path.join(template, 'test.html'), tdict)
    return (ctype, response_body)

def vhost(environ, template):
    ctype = 'text/html'
    #data = augs.Role().read(name="vipbook")['result']['data'][0]['configuration']['files'][0]['data']
    #tdict = {"ServerName": data['ServerName'], "ServerAlias": [ str(alias) for alias in data['ServerAlias'] ], "ServerAdmin": data['ServerAdmin']}
    tdict = {}
    response_body = script.response(os.path.join(template, 'vhost.html'), tdict)
    return (ctype, response_body)

def post(environ, template):
    length = int(environ['CONTENT_LENGTH'])
    data = environ['wsgi.input'].read(length)
    return ('text/plain', data)
