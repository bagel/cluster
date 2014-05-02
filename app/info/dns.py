#!/usr/bin/env python

import os
import sys
import redis
import json
import urllib2
import re
import util2 as util


class Domain:
    def __init__(self):
        self.dnsData = set()

    def domainData(self, domain):
        url = 'http://rdop.matrix.sina.com.cn/dns/index.php/Interface/domain/dname/' + domain
        data = json.loads(urllib2.urlopen(url).read())
        for d in data:
            if d["enabled"] == "false":
                continue
            dns = d["data"]
            attach = d["attach"]
            if not re.match('\d+\.\d+\.\d+\.\d+', dns):
                if d['dynamic'] == 0 and not re.match(r'^group-', attach) and d["type"] == "CNAME" and not re.search('\.$', dns):
                    dns = '.'.join([dns, attach])
                print dns
                self.domainData(dns)
            else:
                self.dnsData.add(dns)
        print self.dnsData

    def domainSet(self):
        r = redis.StrictRedis(util.localenv("REDIS_INFO_HOST"), util.localenv("REDIS_INFO_PORT"))
        domains = eval(r.get('info_domain'))
        dns = {}
        for domain in domains:
            print domain
            self.dnsData = set()
            self.domainData(domain)
            print self.dnsData
            if self.dnsData:
                dns[domain] = list(self.dnsData)
            else:
                dns[domain] = []
            self.dnsData = set()
        if dns:
            print dns
            r.hmset("info_dns", dns)


if __name__ == "__main__":
    #Domain().domainData("vip.book.sina.com.cn")
    Domain().domainSet()
