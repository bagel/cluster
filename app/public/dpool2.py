import sys
import os
import urllib2
import urllib
import json


def ssh(host, cmd):
    data = {"ip": host, "cmd": cmd}
    url = 'http://dpadmin.grid.sina.com.cn/cgi-bin/ssh.py?'
    return urllib2.urlopen(url=url+urllib.urlencode(data)).read()

def dns(domain):
    url = 'http://rdop.matrix.sina.com.cn/dns/index.php/Interface/domain/dname/' + domain
    data = json.loads(urllib2.urlopen(url=url).read())
    return [ [d['attach'], d['type'], d['data']] for d in data ]

def load(vip):
    url = 'http://w5.lb.sina.com.cn/api/api.php?action=info&location=&vip=' + vip
    data = json.loads(urllib2.urlopen(url=url).read())
    member = set()
    for d in data:
        for m in d['poolmember']:
            if not m:
                continue
            if m.split(':')[1].split(',')[0] == '80' and d['poolname'] != 'lvs_pool':
                member.add(m.split(':')[0])
    return [ str(intip(ip)) for ip in member ]

def snat(server):
    print server
    cmd = 'curl http://180.149.136.250/iplookup/get_client_ip.php?format=rip -H "Host: int.dpool.sina.com.cn" -s --connect-timeout 3'
    return ssh(server, cmd)

def intip(ip):
    url = 'http://dpadmin.grid.sina.com.cn/api/serverlist3.php?ip=' + ip
    info = json.loads(urllib2.urlopen(url=url).read())['list']
    if not info:
        return 1
    else:
        return info[0]['ip_in']

def outip(ip):
    url = 'http://dpadmin.grid.sina.com.cn/api/serverlist2.php?ip=' + ip
    info = json.loads(urllib2.urlopen(url=url).read())['list']
    if not info:
        return 1
    else:
        return info[0]['ip_ex']

def gtalk(self, msg):
    data = {'to': ['freetgm@gmail.com'], 'msg': msg}
    print data
    req = urllib2.Request(url='http://10.210.215.69/gtalk/send')
    req.add_data(json.JSONEncoder().encode(data))
    return urllib2.urlopen(req).read()



if __name__ == "__main__":
    print get_serverlist(mod="varnish")
    #print test()
