#!/usr/bin/env python

import redis
import json
import sys
import time

now = time.time()
tmw = now+24*60*60
ymd = time.strftime("%Y%m%d", time.localtime(now))
tymd = time.strftime("%Y%m%d", time.localtime(tmw))
k = 'record_rds_sample_all_%s' % ymd
tk = 'record_rds_sample_all_%s' % tymd
c = redis.StrictRedis(host='r-uf6db21c0dd00ee4.redis.rds.aliyuncs.com', password='')
with open('pids') as f:
    for line in f:
        line = int(line)
        line = str(line)
        #print line
        #line += 1
        #print line
        c.zrem(k, line)
        c.zrem(tk, line)
