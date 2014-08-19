import sys
import os
import redis
import re
import time
import util2 as util


def urlData():
    r = redis.StrictRedis(host=util.localenv("REDIS_STATUS_TEST_HOST"), port=int(util.localenv("REDIS_STATUS_TEST_PORT")))
    datadir = os.path.join(util.localenv("DATA_DIR"), "hive")
    hivefile = os.path.join(datadir, "hive_card_weibo_url_20140819160034.txt")
    regex_url = re.compile('([^\s]+)\s+(\d+)\s+(\d+)')
    fp = open(hivefile, "r")
    data = {}
    while True:
        line = fp.readline()
        if not line:
            break
        url, second, count = re.match(regex_url, line).groups()
        key = "card.weibo.com_%s" % url
        if not data.has_key(key):
            data[key] = {}
        data[key][second] = count

    for k, v in data.iteritems():
        r.hmset(k, v)

    fp.close()


if __name__ == "__main__":
    urlData()
