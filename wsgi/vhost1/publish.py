#!/usr/bin/env python

import sys
import os
import cgi
import orca
import augs
import script
import split


def pub(environ):
    ctype = 'text/plain; charset=utf-8'
    query = environ['QUERY_STRING']
    if not query:
        response_body = 'pub'
        return (ctype, response_body)
    data = cgi.parse_qs(query)
    node = data['node']
    for file in data['file']:
        oc = orca.Orca(node=node, cmd='/etc/dAppCluster/augs.py', parameters=[file])
        oc.tee()
    response_body = '\n'.join(data['node']) + '\n' + '\n'.join(data['file']) + '\n' + 'Publish OK\n'
    return (ctype, response_body)

def post(environ, template):
    ctype = 'text/html; charset=utf-8'
    length = int(environ['CONTENT_LENGTH'])
    #response_body = environ['wsgi.input'].read(length)
    data = cgi.parse_qs(environ['wsgi.input'].read(length))
    data3 = {}
    data3['ServerName'] = split.ServerName(data['ServerName'][0])
    data3['ServerAlias'] = split.ServerAlias(data['ServerAlias'][0])
    data3['ServerAdmin'] = split.ServerAdmin(data['ServerAdmin'][0])
    data3['AliasLog'] = split.AliasLog(data['AliasLog'][0])
    data3['MC'] = split.MC(data['MC'][0])
    data3['RW'] = split.RW(data['RW'][0])
    data3['DB'] = split.DB(data['DB'][0])
    data1 = augs.Role().read(name="vip.book.sina.com.cn")['result']['data'][0]
    data2 = data1['configuration']['files'][0]['data']
    args = ['ServerName', 'ServerAlias', 'ServerAdmin', 'AliasLog', 'MC', 'RW', 'DB']
    d = 0
    for arg in args:
        if data2[arg] != data3[arg]:
            data2[arg] = data3[arg]
            data1['configuration']['files'][0]['data'] = data2
            d = 1
    if d == 1:
        augs.Role().updata(data1)
        val = 'update ok'
    else:
        val = 'no change'
    #response_body += '%s' % data3['ServerAlias']
    #for key, value in data.items():
    #    response_body += '%s: %s\n' % (key, value)
    tdict = {'val': val}
    response_body = script.response(os.path.join(template, 'post.html'), tdict)
    return (ctype, response_body)

def edit(environ, template):
    ctype = 'text/html'
    data = augs.Role().read(name="vip.book.sina.com.cn")['result']['data'][0]['configuration']['files'][0]['data']
    tdict = {"ServerName": data['ServerName'], "ServerAlias": [ str(alias) for alias in data['ServerAlias'] ], "ServerAdmin": data['ServerAdmin'], "AliasLog": data['AliasLog'], "RW": data['RW'], "MC": data['MC'], "DB": data['DB']}
    response_body = script.response(os.path.join(template, 'vhost.html'), tdict)
    return (ctype, response_body)
