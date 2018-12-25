#!/usr/bin/env python


import redis
import json
import sys


c = redis.StrictRedis(host='r-uf633d195be625f4.redis.rds.aliyuncs.com', password='')


cursor = 0

#while True:
r = c.get('cache_post_base_post_88495845')
print r
info = json.loads(r)
print info
    #r = c.scan(cursor, match='record_rds_sample*')
    #for k in r[1]:
    #    pids = c.zrange(k, 0, -1)
    #    for pid in pids:
    #        info = c.get('adm_record_score_%s' % pid)
    #        if info == None:
    #            #print k, pid, 'empty'
    #            continue
    #        info = json.loads(info)
    #        #print k, pid, info.get('v', 'null')
    #        v = info.get('v','null')
    #        if v == 300:
    #            #c.zrem(k, pid)
    #            print k, pid
    #cursor = r[0]
    #if cursor == 0:
    #    break
