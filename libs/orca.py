#!/usr/bin/env python


import sys
import os
import time
import urllib2
import json
import getopt

class Orca:
    def __init__(self, node=[], cmd='', parameters=[], timeout=150, \
                 parallel='Ture', exclusive='False', \
                 host='api.rome.cluster.sina.com.cn'):
        self.node = node
        self.cmd = cmd
        self.parameters = parameters
        self.host = host
        self.timeout = timeout
        self.parallel = parallel
        self.exclusive = exclusive

    def request(self, action, data):
        req = urllib2.Request(url='http://%s/orchestration/%s' % \
                             (self.host, action))
        req.add_header('Content-Type', 'application/json')
        req.add_data(json.JSONEncoder().encode(data))
        return json.loads(''.join(urllib2.urlopen(req).readlines()))
        

    def create(self):
        data = {'nodes': self.node, 'command': self.cmd, \
                'timeout': self.timeout, 'parallel': self.parallel, \
                'exclusive': self.exclusive, 'parameters': self.parameters}
        return self.request('create', data)['result']['id']

    def tee(self, id=''):
        if not id:
            id = self.create()
        data = {'id': id, "nodes": self.node}
        req = self.request('tee', data)
        return (id, req['result'])
        #return self.request('tee', data)

    def cancel(self, id):
        data = {'id': id}
        return self.request('cancel', data)

    def stat(self, id):
        data = {'id': id, 'nodes': self.node}
        return self.request('stat', data)

    def print_tee(self, (id, data)):
        print id
        print
        for d in data:
            if not d:
                continue
            print d['node']
            print d['output']


if __name__ == "__main__":
    #oc = Orca(node=['10.29.10.81'], cmd='ls')
    #print oc.create()
    #oc = Orca(node=['10.29.10.81'], cmd='ps')
    #print oc.tee('94a930b0-7bd6-11e2-a510-69d4b376d6e4')
    if len(sys.argv) == 1:
        sys.exit(0)
    node = sys.argv[1].split(',')
    cmd = sys.argv[2]
    parameters = sys.argv[3:]
    oc = Orca(node=node, cmd=cmd, parameters=parameters)
    oc.print_tee(oc.tee()) 
