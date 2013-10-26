#!/usr/bin/env python

import sys
import os
import urllib2
import json
import getopt
import base64
import time
import shutil
import md5

sys.path.append('/etc/dAppCluster')
import dpool_lib

class Augus:
    def __init__(self, host='augustus.rome.cluster.sina.com.cn', port='80'):
    #def __init__(self, host='10.210.215.170', port='3000'):
        self.host = host
        self.port = int(port)

    def request(self, action, data):
        req = urllib2.Request(url='http://%s:%d/configuration/%s' % \
                             (self.host, self.port, action))
        #print req.get_full_url()
        req.add_header('Content-Type', 'application/json')
        req.add_data(json.JSONEncoder().encode(data))
        #print json.JSONEncoder().encode(data)
        return json.loads(''.join(urllib2.urlopen(req).readlines()))

class Role(Augus):
    def __init__(self):
        Augus.__init__(self)
        self.action = 'role'

    def read(self, name):
        action = os.path.join(self.action, 'read')
        data = {"criteria": {"name": name}}
        return self.request(action, data)

    def update(self, name, includes=[], category='', configuration={}):
        action = os.path.join(self.action, 'update')
        result = self.read(name)['result']
        if result['affected'] == 1:
            result_data = result['data'][0]
            revision = result_data['revision']
            if not category:
                category = result_data['category']
            if not configuration:
                configuration = result_data['configuration']
            if not includes:
                includes =  result_data['includes']
        elif result['affected'] == 0:
            revision = 0
            if not category:
                category = 'node'
            if not configuration:
                configuration = {"files": []}
        data = {"name": name, "category": category, "includes": includes, \
                "configuration": configuration, "revision": revision, \
                "changelog": ""}
        return self.request(action, data)

    def upfile(self, filename):
        action = os.path.join(self.action, 'update')
        f = open(filename, 'r')
        try:
            data = json.loads(f.read(), strict=False)
        except ValueError:
            #print '%s not JSON object' % filename
            sys.exit(1)
        data['revision'] = self.read(data['name'])['result']['data'][0]['revision']
        return self.request(action, data)

    def updata(self, data):
        action = os.path.join(self.action, 'update')
        #print data
        data['revision'] = self.read(data['name'])['result']['data'][0]['revision']
        return self.request(action, data)

    def delete(self, name):
        action = os.path.join(self.action, 'delete')
        data = {"name": name}
        return self.request(action, data)

    def history(self, name):
        action = os.path.join(self.action, 'history')
        revision = self.read(name)['result']['data'][0]['revision']
        data = {"criteria": {"name": name, "revision": {"$lt": revision}}}
        return self.request(action, data)

class Template(Role):
    def __init__(self):
          Role.__init__(self)
          self.action = 'template'

    def update(self, name, content=""):
        action = os.path.join(self.action, 'update')
        data = {"name": name, "revision": 0, "content": content, "changelog": ""}
        return self.request(action, data)

class Generation(Augus):
    def generate(self, node=[], file=[]):
        action = 'generate'
        data = {'nodes': node, 'tags': '', 'configuration': {'files': file}}
        urls = self.request(action, data)['result'][node[0]]['files'][file[0]]
        #return json.loads(urllib2.urlopen(urls).read())
        return base64.b64decode(json.loads(urllib2.urlopen(urls).read())['content'])

    def review(self, node=''):
        action = 'review'
        data = {'node': node}

class Publish(Generation):
    def create(self, file=[]):
        node = dpool_lib.get_intip()
        print node
        data = self.generate(node=[node], file=file)
        name = data['name']
        path = os.path.dirname(data['path'])
        user, group = data['owner'].split(':')
        permission = int(data['permission'], 8)
        print permission
        content = base64.b64decode(data['content'])
        if not os.path.exists(path):
            os.mkdir(path)
        conf = os.path.join(path, name)
        conf_old = '%s.%s' % (conf, time.strftime('%Y%m%d%H%M%S'))
        os.rename(conf, conf_old)
        fp = open(conf, 'w')
        fp.write(content)
        fp.close()
        os.chmod(conf, permission)
        os.chown(conf, shutil.getpwnam(user).pw_uid, shutil.getgrnam(group).gr_gid)
    

def main():
    #print Template().read('apache_test')
    #print Template().upfile('test.json')
    #print Template().update(name="apache_vhost")
    #print Role().read('vip.book.sina.com.cn')
    print Generation().generate(['10.29.10.226'], ['vip.book.sina.com.cn'])
    #Publish().create(['vip.book.sina.com.cn'])
    #print Generation().review('10.29.10.225')
    #print Role().upfile('tj.json')
    #print Role().update(name='10.29.10.226', includes=['tj_main', 'vip.book.sina.com.cn'], category="node")
    #f=open('hosts', 'r')
    #hosts = f.readline().strip().split(' ')
    #f.close()
    #print hosts
    #print Role().update(name="web2", category=" ", includes=hosts)
    #print Role().read(name="vipbook")['result']['data'][0]['configuration']['files'][0]['data']
    #try:
    #    print Role().delete(name=sys.argv[1])
    #except:
    #    sys.exit(0)
    #print Role().update(name="vip.book.sina.com.cn", category= " ")


if __name__ == '__main__':
    main()
