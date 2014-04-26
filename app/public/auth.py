import sys
import os
import redis
import web
import util


class _Auth(object):
    """auth if user has permission to domain"""
    def __init__(self, environ, domain):
        self.user = environ["USER"]
        self.host = environ["HTTP_HOST"]
        self.domain = domain
        self.r = redis.StrictRedis(web.getenv("REDIS_INFO_HOST"), int(web.getenv("REDIS_INFO_PORT")))

    def authdomain(self, err):
        """if user in dpool or is domains admin or in domains users has permission"""
        user_admin = self.r.get("info_dpool_admin")
        #print self.user, user_admin
        if user_admin and self.user in eval(user_admin):
            return self.user
        domains_admin = self.r.hget("info_domain_admin", self.user)
        if domains_admin and self.domain in eval(domains_admin):
            return self.user
        domains = self.r.hget("info_domain_user", self.user)
        if not domains:
            return err
        domains = eval(domains)
        if self.domain in domains:
            return self.user
        return err

    def auth(self):
        """api visit return json format error"""
        if self.host == "api.dpool.cluster.sina.com.cn":
            return self.authdomain(web.error.errapi(403))
        else:
            return self.authdomain(web.error.errweb(403))


def authdomain(user, domain):
    return _Auth(user, domain).auth()
