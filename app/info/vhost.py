#!/usr/bin/env python

import sys
import os
import redis
import urllib2
import re
import socket
import ConfigParser

def confData(conf):
    url = 'http://dpadmin.grid.sina.com.cn/api/fetch_newestfile.php?title=' + conf
    return urllib2.urlopen(url, timeout=3)

def vhostWeb3Data():
    vhostConf = {}
    f = confData('fpm.conf.vhost')
    line = f.readline()
    while line:
        if re.match(r'<fpm\s+[\w\.\_\-]+>', line):
            domain = re.sub(r'<fpm\s+([\w\.\_\-]+)\s*>\s*\n', r'\1', line)
            if not vhostConf.has_key(domain):
                vhostConf[domain] = {}
            while line:
                line = f.readline()
                if re.match(r'env\[SINASRV_DB\d*_PASS', line):
                    continue
                elif re.match(r'env\[SINASRV_(DB|REDIS)', line):
                    k, v = re.sub(r'env\[([\w\_]+)\]\s+=\s+\"([\w\.\_\@\s\_\-]+)\"\s*\n', r'\1 \2', line).strip().strip().split(' ')[:2]
                    vhostConf[domain][k] = v
                elif re.match('</fpm>', line):
                    break
        line = f.readline()
    return vhostConf

def vhostWeb2Data():
    vhostConf = {}
    f = confData('web2_httpd_vhost.conf')
    line = f.readline()
    while line:
        if re.match(r'\s+ServerName\s+@@[\w\.\_\-]+@@', line):
            domain = re.sub(r'\s+ServerName\s+@@([\w\.\_\-]+)@@\s*\n', r'\1', line)
            if not vhostConf.has_key(domain):
                vhostConf[domain] = {}
            while line:
                line = f.readline()
                if re.match(r'\s+SetEnv SINASRV_DB\d*_PASS', line):
                    continue
                elif re.match(r'\s+SetEnv\s+SINASRV_(DB|REDIS)\w+\s+\"?[\w\.\@\s\_\-]+\"?', line):
                    k, v = re.sub(r'\s+SetEnv\s+([\w\_]+)\s+\"?([\w\.\@\s\_\-]+)\"?\s*\n', r'\1 \2', line).strip().strip().split(' ')[:2]
                    vhostConf[domain][k] = v
                elif re.match(r'\s*</VirtualHost>', line):
                    break
        line = f.readline()
    return vhostConf

def envData(data):
    env = {}
    if not data:
        return env
    region = ["mars", "apollo", "atlas", "aries"]
    for k, v in data.iteritems():
        if not re.match(r'SINASRV_(DB|REDIS)', k):
            continue
        db, sql, item = re.sub(r'SINASRV_((DB|REDIS)[a-zA-Z0-9]*)_([\w\_]+)', r'\1 \2 \3', k).split(' ')
        sql = sql.lower()
        if not env.has_key(sql):
            env[sql] = {}
        if not env[sql].has_key(db):
            env[sql][db] = {}
        if re.search(r'(HOST|HOST_R)$', k):
            grid = []
            for reg in region:
                g = '.'.join([re.sub('([\w]+)\.@@.*', r'\1', v), '%s.grid.sina.com.cn' % reg])
                try:
                    grid.extend(socket.gethostbyname_ex(g)[2])
                except socket.gaierror:
                    pass
            env[sql][db][item.lower().replace('host', 'hostip')] = list(set(grid))
            if '@@' in v:
                v = '.'.join([re.sub('([\w]+)\.@@.*', r'\1', v), '%s.grid.sina.com.cn' % region[0]])
            else:
                v = '.'.join([re.sub('([\w]+)\..*', r'\1', v), '%s.grid.sina.com.cn' % region[0]])
        env[sql][db][item.lower()] = v
    return env

def mcData():
    mc = {}
    f = confData('dpool_mcheck.conf')
    line = f.readline()
    while line:
        if re.match('\s*#', line) or not line.strip() or '|' not in line:
            line = f.readline()
            continue
        domain = line.split(':')[4].split('|')[0]
        if not mc.has_key(domain):
            mc[domain] = {}
        server, var, idc = re.sub(r'(\d+\.\d+\.\d+\.\d+\:\d+)\:[\d\w]+\:\w+\:%s\|SINASRV_([\w\_]+)_SERVERS\|([a-zA-Z]+).*\n' % domain, r'\1 \2 \3', line).split(' ')
        if not mc[domain].has_key(var):
            mc[domain][var] = {}
        if not mc[domain][var].has_key(idc):
            mc[domain][var][idc] = []
        mc[domain][var][idc].append(server)
        line = f.readline()
    return mc

def vhostSet():
    r = redis.StrictRedis("10.13.32.21")
    data = {}
    mc = mcData()
    for k, v in vhostWeb3Data().iteritems():
        data[k] = envData(v)
        data[k]["pool"] = "web3"
        data[k]["mc"] = mc.get(k, mc["web3"])
    for k, v in vhostWeb2Data().iteritems():
        if data.has_key(k):
            continue
        data[k] = envData(v)
        data[k]["pool"] = "web2"
        data[k]["mc"] = mc.get(k, mc["dpool"])
    if data:
        print data
        r.hmset("info_vhost", data)

    return data

if __name__ == "__main__":
    vhostSet()
