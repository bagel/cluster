import sys
import os
import redis
import hashlib
import urlparse
import json
import time
import web
import util

class Profile(object):
    def __init__(self, environ):
        self.environ = environ
        self.user = self.environ["USER"]
        self.r = redis.StrictRedis('10.13.32.21', 6381)
        self.query = urlparse.parse_qs(self.environ["QUERY_STRING"])
        self.key_user = "info_domain_user"
        self.key_domain = "info_user_domain"
        self.key_admin = "info_domain_admin"
        self.key_dpool = "info_dpool_admin" 
        self.key_status = "info_domain_status"

    def domainAuth(self):
        """post /profile/domainauth(add|del), {"domains": domains, "users": users},
           "all" for all admin domain, if domain is servername, serveralias will be included.
        """
        postData = json.loads(self.environ['wsgi.input'].read(int(self.environ['CONTENT_LENGTH'])))
        domains = postData["domains"].strip().split(',')
        domains_admin = self.r.hget(self.key_admin, self.user)
        if domains_admin:
            domains_admin = eval(domains_admin)
        else:
            domains_admin = []
        dpool_admin = self.r.get(self.key_dpool)
        if dpool_admin:
            dpool_admin = eval(dpool_admin)
        else:
            dpool_admin = []
        domains_new = set()
        for domain in domains:
            domain = domain.strip()
            domain_server = self.r.hget("info_domainserver", domain)
            if domain == "all":
                if domains_admin:
                    domains_new.update(domains_admin)
                break
            elif domain not in domains_admin and self.user not in dpool_admin:
                continue
            elif domain_server and eval(domain_server):
                domains_new.update(eval(domain_server))
                domains_new.update([domain])
            else:
                domains_new.update([domain])
        users = postData["users"].strip().split(',')
        return (domains_new, users)

    @web.response
    def domainAuthAdd(self):
        """add domain to info_domain_user, {"user prefix": [domains]},
           add user to info_user_domain, {"domain": [users]}.
        """
        domains, users = self.domainAuth()
        for d in domains:
            if not d:
                continue
            for u in users:
                if '@' not in u:
                    u = '@'.join([u, "staff.sina.com.cn"])
                u_head = u.strip().split('@')[0]
                if not self.r.hexists(self.key_user, u_head):
                    self.r.hset(self.key_user, u_head, [d])
                else:
                    ds = eval(self.r.hget(self.key_user, u_head))
                    if d not in ds:
                        ds.append(d)
                        self.r.hset(self.key_user, u_head, ds)
                if not self.r.hexists(self.key_domain, d):
                    self.r.hset(self.key_domain, d, [u])
                else:
                    us = eval(self.r.hget(self.key_domain, d))
                    if u not in us:
                        us.append(u)
                        self.r.hset(self.key_domain, d, us)
        return ("application/json", json.JSONEncoder().encode({"success": 0}))

    @web.response
    def domainAuthDel(self):
        """remove domain from info_domain_user, user from info_user_domain.
        """
        domains, users = self.domainAuth()
        for d in domains:
            if not d:
                continue
            for u in users:
                if '@' not in u:
                    u = '@'.join([u, "staff.sina.com.cn"])
                u_head = u.strip().split('@')[0]
                if not self.r.hexists(self.key_user, u_head):
                    continue
                else:
                    ds = eval(self.r.hget(self.key_user, u_head))
                    if d in ds:
                        ds.remove(d)
                        self.r.hset(self.key_user, u_head, ds)
                if not self.r.hexists(self.key_domain, d):
                    continue
                else:
                    us = eval(self.r.hget(self.key_domain, d))
                    if u in us:
                        us.remove(u)
                        self.r.hset(self.key_domain, d, us)
        return ("application/json", json.JSONEncoder().encode({"success": 0}))

    def domainUser(self):
        domains = set()
        domain_admin = self.r.hget(self.key_admin, self.user)
        if domain_admin:
            domain_admin = eval(domain_admin)
            domains.update(domain_admin)
        domain_user = self.r.hget(self.key_user, self.user)
        if domain_user:
            domain_user = eval(domain_user)
            domains.update(domain_user)
        return domains

    def domainStat(self, start=0, num=10):
        """domains that user admin and user has permission, include every domain's users,
           {"example.com": ["caoyu2", ...], ... }
        """
        domains = self.domainUser()
        domain_stat = []
        domains = sorted(list(domains))
        count = len(domains)
        domains = domains[start:start+num]
        for domain in domains:
            stat = self.r.hget(self.key_domain, domain)
            if stat:
                stat = eval(stat)
                stat = ','.join([ u.split('@')[0] for u in stat ])
            else:
                stat = ""
            domain_stat.append([domain, stat])
        return (domain_stat, count)

    @web.response
    def responseStat(self):
        """if no query then response count of domains.
        """
        start = int(self.query.get("start", [0])[0])
        num = int(self.query.get("num", [0])[0])
        if num == 0:
            return ("application/json", json.JSONEncoder().encode({"count": self.domainStat(start, num)[1]}))
        else:
            return ("application/json", json.JSONEncoder().encode(self.domainStat(start, num)[0]))

    @web.response
    def responseStatDomain(self):
        """check one domain permit users.
        """
        domain = self.query.get("domain", [""])[0]
        stat = self.r.hget(self.key_domain, domain)
        if stat:
            stat = eval(stat)
            stat = ','.join([ u.split('@')[0] for u in stat ])
        else:
            stat = ""
        return ("application/json", json.JSONEncoder().encode({domain: stat}))

    def domainStatus(self, domain):
        """uri and rtime in domain status that user admin and user has permission.
           {"example.com": {"uri": ["/test"], "rtime": [[0, 0.1], [0.1, 1000]], "uri_rtime":...}
        """
        domain_status = []
        status = self.r.hget(self.key_status, domain)
        if status:
            status = eval(status)
            if status.has_key("uri"):
                for u in status["uri"]:
                    domain_status.append([domain, u, ""])
            if status.has_key("rtime"):
                for rtime in status["rtime"]:
                    domain_status.append([domain, "", "~".join([str(rt) for rt in rtime]) + "s"])
            if status.has_key("uri_rtime"):
                for u in status["uri_rtime"].iterkeys():
                    for rtime in status["uri_rtime"][u]:
                        domain_status.append([domain, u, "~".join([str(rt) for rt in rtime]) + "s"])
        return domain_status

    @web.response
    def responseStatus(self):
        """if no query then response count of domains has status.
        """
        start = int(self.query.get("start", [0])[0])
        num = int(self.query.get("num", [0])[0])
        domains = self.query.get("domain", [])
        if not domains:
            domains = self.domainUser()
        domain_status = []
        for domain in domains:
            domain_status.extend(self.domainStatus(domain))
        count = len(domain_status)
        domain_status = domain_status[start:start+num]
        if not self.query.has_key("num"):
            return ("application/json", json.dumps({"count": count}))
        else:
            return ("application/json", json.dumps(domain_status))

    @web.response
    def response(self):
        key = util.userkey(self.user)
        return ("text/html", web.template(self.environ, "profile.html", {"key": key, "domainStat": self.domainStat()}))
