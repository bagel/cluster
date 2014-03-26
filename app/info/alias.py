#!/usr/bin/env python

import os
import sys
import redis
import json
import urllib2
import re


def confData(conf):
    url = 'http://dpadmin.grid.sina.com.cn/api/fetch_newestfile.php?title=' + conf
    return urllib2.urlopen(url, timeout=3)

def aliasWeb3():
    aliasData = {}
    serverData = {}
    f = confData('nginx.conf.vhost_fpm')
    line = f.readline()
    while line:
        if re.match('\s*server_name', line):
            domains = re.sub(r'^\s*server_name\s+@@.*@@\s+([\w\.\s\-\_]+)\s*;\s*\n', r'\1', line).strip().split(' ')
            servername = domains[0]
            domains.remove(servername)
            serverData[servername] = domains
            for domain in domains:
                aliasData[domain] = servername
        line = f.readline()
    return (aliasData, serverData)

def aliasWeb2():
    aliasData = {}
    serverData = {}
    f = confData('web2_httpd_vhost.conf')
    line = f.readline()
    while line:
        if re.match('\s*#', line):
            line = f.readline()
            continue
        if re.match('\s*ServerName', line):
            servername = re.sub('^\s*ServerName\s+@@([\w\.\-\_]+)@@\s*\n', r'\1', line).strip()
        if re.match('\s*ServerAlias', line):
            serveralias = re.sub('^\s*ServerAlias\s+@*([\w\.\-\_]+)@*\s*\n', r'\1', line).strip()
            if not servername:
                line = f.readline()
                continue
            aliasData[serveralias] = servername
            if not serverData.has_key(servername):
                serverData[servername] = []
            serverData[servername].append(serveralias)
        if re.search('</VirtualHost>', line):
            aliasData[servername] = servername
            if not serverData.has_key(servername):
                serverData[servername] = []
            servername = ''
        line = f.readline()
    return (aliasData, serverData)

def aliasUpdate():
    alias, server = aliasWeb3()
    alias2, server2 = aliasWeb2()
    alias.update(alias2)
    server.update(server2)
    r = redis.StrictRedis('10.13.32.21', 6379)
    r.hmset('info_domainalias', alias)
    r.hmset('info_domainserver', server)


if __name__ == "__main__":
    aliasUpdate()
