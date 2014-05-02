import sys
import os
import yaml


def localenv(key):
    conf = "/data1/www/htdocs/admin.dpool.cluster.sina.com.cn/conf/main.yaml"
    with open(conf, "r") as fp:
        envs = yaml.load(fp.read())
    for k, v in envs.iteritems():
        if k == key:
            return v
    return None

