#!/usr/bin/env python
# coding: utf-8

import sys
import os
import time
import urllib2
import memcache
import json

sys.path.append('/data1/www/htdocs/api.dpool.cluster.sina.com.cn/libs/')
import shortcut
import mc

class IPList:
    def __init__(self):
        self.idc = {'xd': '西单', 'ja': '静安', 'gd': '广东', 'sh': '上海', 'yf': '永丰', 'tc': '土城', 'edu': '教育网', 'bx': '北显'}

    def getVip(self, domain):
        vip = set()
        [ vip.add(v[2]) for v in shortcut.dns(domain) ]
        return list(vip)

    def getMember(self, vip):
        member = []
        net = []
        check_url = 'http://api.dpool.cluster.sina.com.cn/online?ip='
        for m in shortcut.load(vip):
           m = shortcut.intip(m)
           if m == 1:
               continue
           if '.'.join(m.split('.')[:3]) not in net and urllib2.urlopen(url=check_url+m).read().strip() == "1101":
               net.append('.'.join(m.split('.')[:3]))
               member.append(m)
        return member

    def getMemberAll(self, vip):
        member = []
        for m in shortcut.load(vip):
            m = shortcut.intip(m)
            if m != 1:
                member.append(str(m))
        return member

    def getSnat(self, vip, ex=0):
        snat = mc.get('snat')
        if not snat:
            if ex == 1:
                snat = 0
            else:
                snat = mc.get("snat_b")
        if not snat:
            snat = {}
            for v in vip:
                print v
                s = set()
                for m in shortcut.load(v):
                    t = shortcut.snat(shortcut.intip(m)).strip()
                    if t != "1" and t:
                        s.add(t)
                snat.update({v: list(s)})
                print snat
            mc.set('snat', snat, 3600)
            mc.set('snat_b', snat, 5400)
        return snat

    def getIdc(self, ip):
        net = int(ip.split('.')[1])
        if net == 55:
            return self.idc['xd']
        elif net == 69:
            return self.idc['ja']
        elif net == 71:
            return self.idc['gd']
        elif net == 73:
            return self.idc['tc']
        elif net == 79:
            return self.idc['yf']
        elif net == 6:
            return self.idc['edu']
        elif net == 53:
            return self.idc['sh']
        else:
            return 'Unkown'

    def Summary(self, environ, ex=0):
        vip = list(set(self.getVip('common7.dpool.sina.com.cn') + self.getVip('common6.dpool.sina.com.cn')))
        print vip
        snat = self.getSnat(vip, ex)
        print snat
        sum = mc.get('sum')
        mems = mc.get('mems')
        if not sum:
            if ex == 1:
                sum = 0
            else:
                sum = mc.get('sum_b')
        if not sum: 
            sum = {}
            for v in vip:
                member = self.getMember(v)
                sum.update({v: {"member": member, "snat": snat[v]}})
            mc.set('sum', sum, 3600)
            mc.set('sum_b', sum, 5400)
        print sum
        if not mems:
            if ex == 1:
                mems = 0
            else:
                mems = mc.get('mems_b')
        if not mems:
            mems = {}
            for v in vip:
                mem = self.getMemberAll(v)
                mems.update({self.getIdc(mem[0]): mem})
            mc.set('mems', mems, 3600)
            mc.set('mems_b', mems, 5400)
        print mems 
        ctype = 'text/plain; charset=utf-8'
        response_body = ''
        snat = []
        member = []
        sum_n = {}
        for ivip, val in sum.items():
            snat += val['snat']
            member += val['member']
            idc = self.getIdc(val['member'][0])
            response_body += "%s\nVIP:%s\nSNAT:%s\nmember:%s\n\n" % (idc, str(ivip), ', '.join(val['snat']), ', '.join([ str(m) for m in val['member'] ]))
            sum_n.update({idc: {"vip": ivip, "snat": val['snat'], "member": val['member']}})
        response_body += "\nSNAT:%s\n" % ', '.join(snat)
        response_body += "\nNET:%s\n" % ', '.join([ '.'.join(str(m).split('.')[:3]) + '.0/24' for m in member ])
        if environ['QUERY_STRING'] == 'snat':
            response_body = '\n'.join(snat) + '\n'
        elif environ['QUERY_STRING'] == 'all':
            memlist = []
            for m in mems.values():
                memlist += m
            response_body = '\n'.join(memlist) + '\n'
        elif environ['QUERY_STRING'] in self.idc.keys():
            print self.idc[environ['QUERY_STRING']]
            response_body = '\n'.join(mems[self.idc[environ['QUERY_STRING']]]) + '\n'
        elif environ['QUERY_STRING'] == 'vip':
            print vip
            response_body = '\n'.join([ str(v) for v in vip ]) + '\n'
        elif environ['QUERY_STRING'] == 'net':
            response_body = '\n'.join([ '.'.join(str(m).split('.')[:3]) + '.0/24' for m in member ]) + '\n'
        elif environ['QUERY_STRING'] == 'json':
            ctype = "application/json; charset=utf-8"
            response_body = json.JSONEncoder().encode(sum_n)
        print sum_n
        return (ctype, response_body)
        

if __name__ == "__main__":
    #print IPList().getVip()
    #print IPList().getMember('218.30.115.176')
    #print IPList().getSnat('10.69.6.90')
    environ = {}
    environ['SINASRV_MEMCACHED_SERVERS'] = "10.13.32.22:7601"
    environ['QUERY_STRING'] = ""
    os.environ['MEMCACHE_SERVERS'] = "10.13.32.22:7601"
    os.environ['SINASRV_MEMCACHED_SERVERS'] = "10.13.32.22:7601"
    print IPList().Summary(environ, 1)
#test2
