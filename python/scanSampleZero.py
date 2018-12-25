#!/usr/bin/env python

import time
import redis
import json
import sys


c = redis.StrictRedis(host='r-uf6db21c0dd00ee4.redis.rds.aliyuncs.com', password='')

f = open('leftsamplecount.txt', 'a+')

try: 
    while True:
        now = time.time()
        tmw = now+24*60*60
        ymd = time.strftime("%Y%m%d", time.localtime(now))
        tymd = time.strftime("%Y%m%d", time.localtime(tmw))
        k = 'record_rds_sample_all_%s' % ymd
        tk = 'record_rds_sample_all_%s' % tymd

        cnt = c.zcard(k)
        tcnt = c.zcard(tk)
        f.write("%s: count %d, tcount %d\n"%(time.strftime("%Y%m%d,%H:%M:%S",time.localtime(time.time())), cnt, tcnt))
        f.flush()
        time.sleep(30)
except (KeyboardInterrupt, SystemExit):
    f.close()
    sys.exit()
