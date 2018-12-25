#!/usr/bin/env python


import redis
import json
import sys


c = redis.StrictRedis(host='r-uf6db21c0dd00ee4.redis.rds.aliyuncs.com', password='')
cursor = 0

while True:
    r = c.scan(cursor, match='record_rds_sample_all_20181216')
    for k in r[1]:
        pids = c.zrange(k, 0, -1)
        for pid in pids:
            info = c.get('adm_record_score_%s' % pid)
            if info == None:
                #print k, pid, 'empty'
                continue
            info = json.loads(info)
            #print k, pid, info.get('v', 'null')
            stage = info.get('stage','null')
            if stage == 1:
                ct = info.get('ct','null')
                if ct < 1544878800:
                    c.zrem(k, pid)
                    c.delete('adm_record_score_%s'%pid)
                    print k, pid
    cursor = r[0]
    if cursor == 0:
        break
