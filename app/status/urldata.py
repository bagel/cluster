import sys
import os
import redis
import re
import time
import util2 as util


def urlData():
    r = redis.StrictRedis(host=util.localenv("REDIS_STATUS_TEST_HOST"), port=int(util.localenv("REDIS_STATUS_TEST_PORT")))
    datadir = os.path.join(util.localenv("DATA_DIR"), "hive")
    day = time.strftime("%Y%m%d")
    yday = time.strftime("%Y%m%d", time.localtime(time.time() - 86400))
    hivefile = os.path.join(datadir, "card_weibo_url_hits_%s/hive_card_weibo_url_hits_%s010000" % (day, day))
    regex_url = re.compile('([^\s]+)\s+(\d+)\s+(\d+)')
    fp = open(hivefile, "r")
    data = {}
    while True:
        line = fp.readline()
        if not line:
            break
        url, second, count = re.match(regex_url, line).groups()
        key = "%s_card.weibo.com_%s" % (yday, url)
        if not data.has_key(key):
            data[key] = []
        data[key].append([second, count])

    for k, v in data.iteritems():
        r.set(k, v)

    fp.close()


if __name__ == "__main__":
    urlData()
