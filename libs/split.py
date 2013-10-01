#!/usr/bin/env python

import sys
import os
import re
import cStringIO


def ServerName(s):
    return s.split('ServerName')[-1].strip()

def ServerAlias(s):
    return [ alias.strip().split('ServerAlias')[-1].strip() for alias in s.split('\r\n') if alias ]

def ServerAdmin(s):
    return s.split('ServerAdmin')[-1].strip()

def AliasLog(s):
    aliaslog = []
    for line in s.split('\r\n'):
        if re.match('\s*SetEnvIf\s+Host', line):
            Name, Group = [ k.strip('"') for k in line.strip().split(' ') if k and k != '"' ][-2:]
            aliaslog.append({"AliasName": Name, "AliasGroup": Group})
    return aliaslog

def MC(s):
    mc = []
    for line in s.split('\r\n'):
        if re.match('\s*SetEnv\s+SINASRV_MEMCACHED.*_SERVERS', line):
            N = line.split('MEMCACHED')[1].split('_SERVERS')[0]
            SERVERS = []
            for SERVER, PORT in [ k.split(':') for k in line.split('_SERVERS')[-1].strip().strip('"').split() ]:
                SERVERS.append({'SERVER': SERVER, 'PORT': PORT})
            mc.append({'N': N, "SERVERS": SERVERS})
    return mc

def RW(s):
    rw = []
    for line in s.split('\r\n'):
        if re.match('\s*RewriteCond', line):
            K = [ k for k in line.split('RewriteCond')[-1].strip().split(' ') if k ]
            P = T = F = ""
            if len(K) == 2:
                P, T = K
            elif len(K) == 3:
                P, T, F = K
            rw.append({"O": "Cond", "P": P, "T": T, "F": F})
        if re.match('\s*RewriteRule', line):
            K = [ k for k in line.split('RewriteRule')[-1].strip().split(' ') if k ]
            P = T = F = ""
            if len(K) == 2:
                P, T = K
            elif len(K) == 3:
                P, T, F = K
            rw.append({"O": "Rule", "P": P, "T": T, "F": F})
    return rw

def DB(s):
    Db = []
    f = cStringIO.StringIO()
    f.write(s)
    f.seek(0)
    line = f.readline()
    while line:
        if re.match('\s*SetEnv\s+SINASRV_DB', line):
            db = ''
            d = {}
            db = [ k for k in line.strip().split(' ') if k ][1].split('_')[1]
            d.update({'N': db.lstrip('DB')})
            while line:
                if re.match('\s*SetEnv\s+SINASRV_%s' % db, line):
                    dt = [ k for k in line.strip().split(" ") if k ]
                    ds = dt[1].split('_')
                    if len(ds) == 3:
                        if ds[-1] != "HOST":
                            d.update({ds[-1]: dt[-1]})
                    elif len(ds) == 4:
                        if '_'.join(ds[-2:]) != "HOST_R":
                            d.update({'_'.join(ds[-2:]): dt[-1]})
                #elif not line.strip():
                #    pass
                else:
                    Db.append(d)
                    break
                line = f.readline()
            continue
        line = f.readline()
    return Db
