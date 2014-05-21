import sys
import os
import redis
import urlparse
import time
import web
import json


class Custom(object):
    def __init__(self, environ):
        self.environ = environ
        self.user = self.environ["USER"]
        self.r = redis.StrictRedis(host=web.getenv("REDIS_INFO_HOST"), \
                                   port=int(web.getenv("REDIS_INFO_PORT")))
        self.query = urlparse.parse_qs(self.environ["QUERY_STRING"])
        self.key_user = "info_domain_user"
        self.key_domain = "info_user_domain"
        self.key_admin = "info_domain_admin"
        self.key_dpool = "info_dpool_admin"
        self.key_status = "info_domain_status"

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

    def getStatus(self):
        postData = json.loads(self.environ['wsgi.input'].read(int(self.environ['CONTENT_LENGTH'])))
        domain = postData.get("domain", "").encode('utf-8')
        uri = postData.get("uri", "").encode('utf-8')
        rmin = postData.get("rmin", "").encode('utf-8')
        rmax = postData.get("rmax", "").encode('utf-8')
        if rmin and float(rmin).is_integer():
            rmin = int(float(rmin))
        elif rmin:
            rmin = float(rmin)
        if rmax and float(rmax).is_integer():
            rmax = int(float(rmax))
        elif rmax:
            rmax = float(rmax)
        return (domain, uri, rmin, rmax)

    @web.response
    def addStatus(self):
        """add domain uri or rtime status"""
        ctype = "application/json"
        domain, uri, rmin, rmax = self.getStatus()
        rtime = []
        if rmin and rmax:
            if rmin > rmax:
                return (ctype, json.dumps({"msg": "error"}))
            rtime = [rmin, rmax]
        elif rmin:
            rtime = [rmin, 10000]
        elif rmax:
            rtime = [0, rmax]
        if not domain or (not uri and not rtime):
            return (ctype, json.dumps({"msg": "error"}))
        status = self.r.hget(self.key_status, domain)
        if status:
            status = eval(status)
        else:
            status = {}
        if uri and rtime:
            if not status.has_key("uri_rtime"):
                status["uri_rtime"] = {}
            if not status["uri_rtime"].has_key(uri):
                status["uri_rtime"][uri] = []
            if rtime not in status["uri_rtime"][uri]:
                status["uri_rtime"][uri].append(rtime)
        elif uri:
            if not status.has_key("uri"):
                status["uri"] = []
            if uri not in status["uri"]:
                status["uri"].append(uri)
        elif rtime:
            if not status.has_key("rtime"):
                status["rtime"] = []
            if rtime not in status["rtime"]:
                status["rtime"].append(rtime)
        self.r.hset(self.key_status, domain, status)
        return (ctype, json.dumps({"msg": "success"}))

    @web.response
    def delStatus(self):
        """add domain uri or rtime status"""
        ctype = "application/json"
        domain, uri, rmin, rmax = self.getStatus()
        rtime = []
        if rmin and rmax:
            if rmin > rmax:
                return (ctype, json.dumps({"msg": "error"}))
            rtime = [rmin, rmax]
        elif rmin:
            rtime = [rmin, 10000]
        elif rmax:
            rtime = [0, rmax]
        if not domain or (not uri and not rtime):
            return (ctype, json.dumps({"msg": "error"}))
        status = self.r.hget(self.key_status, domain)
        if status:
            status = eval(status)
        else:
            return (ctype, json.dumps({"msg": "error"}))
        if uri and rtime:
            if status.has_key("uri_rtime") and status["uri_rtime"].has_key(uri) and \
                                               rtime in status["uri_rtime"][uri]:
                status["uri_rtime"][uri].remove(rtime)
            else:
                return (ctype, json.dumps({"msg": "error"}))
        elif uri:
            if status.has_key("uri") and uri in status["uri"]:
                status["uri"].remove(uri)
            else:
                return (ctype, json.dumps({"msg": "error"}))
        elif rtime:
            if status.has_key("rtime") and rtime in status["rtime"]:
                status["rtime"].remove(rtime)
            else:
                return (ctype, json.dumps({"msg": "error"}))
        self.r.hset(self.key_status, domain, status)
        return (ctype, json.dumps({"msg": "success"}))
    

    @web.response
    def response(self):
        return ("text/html", web.template(self.environ, "custom.html"))

