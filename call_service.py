#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymongo
import optparse
import sys
import requests
import json
import datetime
import time
import ujson
import threading
import redis
import urllib2

reload(sys)
sys.setdefaultencoding('utf8')

def call_service(service_url, data):
    req = urllib2.Request(service_url)
    req.add_header('Content-Type', 'application/json')

    strdata = ujson.dumps(data)
    try:
        response = urllib2.urlopen(req, strdata)
    except Exception, e:
        print "http request error %s, data %s" % (service_url, str(e))
        return None

    code = response.getcode()
    if code != 200:
        print 'bad response, code %d, data %s' % (code, strdata)
        return None

    resp = response.read()
    try:
        r = ujson.loads(resp)
    except Exception:
        print "bad response %s, data %s" % (resp, strdata)
        return None

    if r==None: return None

    ret = r.get('ret', None)
    if ret != 1:
        ret = r.get('errcode', None)

    if None == ret:
        print 'call service failed, ret is None, resp %s, url %s, data %s' % (resp, service_url, strdata)
        return None

    if ret != 1:
        print 'call service failed, ret %d, resp %s, url %s, data %s' % (ret, resp, service_url, strdata)
        return None

    return r

def get_redis(host, port, db=0, password=None):
    pool = redis.ConnectionPool(host=host, port=port, db=db, password=password)
    redis_conn = redis.Redis(connection_pool=pool)
    return redis_conn


def main():
    start_time = int(time.time())

    url_get_active_status_by_ids = ''
    param = {}
    ret = call_service(url_get_active_status_by_ids, param)
    if not ret or ret.get('ret',0) != 1:
        print ""
        return




if __name__ == '__main__':
    main()
