#!/usr/bin/env python

import sys
import os
import redis
import MySQLdb
import time
import re


r = redis.StrictRedis(host='10.13.32.21', port=6379)
conn = MySQLdb.connect(host="10.13.32.21", user="root", passwd="123456", port=3306, db="hits")
cu = conn.cursor()

t0 = int(time.time())
t0 = t0 - t0 % 60

t = t0 = t0 - 86400 - 3600
while t > t0 - 3600 - 1200:
    print t

    day = time.strftime('%Y%m%d', time.localtime(t))
    try:
        cu.execute('desc `%s`', int(day))
    except:
        cu.execute('create table `%s` (host varchar(20), domain varchar(100), time int(10) unsigned, hits int(10) unsigned) engine=innodb default charset=utf8', int(day))
        conn.commit()

    for k, v in r.hgetall(t).items():
        if re.match(r'\d+\.\d+\.\d+\.\d+', k):
            cu.execute('insert into `%s` (host, time, hits) values (%s, %s, %s)', (int(day), k, t, v))
        else:
            cu.execute('insert into `%s` (domain, time, hits) values (%s, %s, %s)', (int(day), k, t, v))
    r.delete(t)

    for key in r.keys("%s_*" % t):
        for k, v in r.hgetall(key).items():
            cu.execute('insert into `%s` (host, domain, time, hits) values (%s, %s, %s, %s)', (int(day), key.split('_')[-1], k, t, v))
        r.delete(key)

    conn.commit()

    t -= 60

cu.close()
conn.close()
