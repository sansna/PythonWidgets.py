#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 May 16 11:54:29

import time
import consul
import requests
import ujson
import jq

now = int(time.time())
today = int(now+8*3600)/86400*86400-8*3600
dayts = 86400
hourts = 3600
mints = 60
yesterday = today - dayts

istest = True

#gw/frontend
GWACNT = "hanabi-acnt.api.ns"
GWCOMM = "hanabi-gateway.api.ns"
GWMATCH = "hanabi-matcher.api.ns"
GWMESG = "hanabi-message.api.ns"
GWMEDIA = "hanabi-media-gateway"
OPAPI = "hanabi-opapi"
#srv
BIZACNT = "hanabi-bizsrv-acnt"
BIZANTI = "hanabi-bizsrv-antispam"
BIZATT = "hanabi-bizsrv-attention"
BIZCOMM = "hanabi-bizsrv"
BIZMATCH = "hanabi-bizsrv-matcher"
BIZPOST = "hanabi-bizsrv-post"
BIZRECORD = "hanabi-bizsrv-record"
BIZREVIEW = "hanabi-bizsrv-review"
BIZCHAT = "hanabi-chatsrv-core"
BIZCHATPUSH = "hanabi-chatsrv-push"
BIZCHATSTOR = "hanabi-chatsrv-storage"
BIZMEDIASTOR = "hanabi-media-storage"
BIZMEDIACONV = "hanabi-media-convert"
if istest:
    #gw/frontend
    GWACNT = "hanabi-acnt.api.ns"
    GWCOMM = "hanabi-acnt.api.ns"
    GWMATCH = "hanabi-matcher.api.ns"
    GWMESG = "hanabi-acnt.api.ns"
    GWMEDIA = "hanabi-media-gateway.srv.ns"
    OPAPI = "hanabi-opapi"
    #srv
    BIZACNT = "hanabi-acnt.srv.ns"
    BIZANTI = "hanabi-antispam.srv.ns"
    BIZATT = "hanabi-attention.srv.ns"
    BIZCOMM = "hanabi-acnt.srv.ns"
    BIZMATCH = "hanabi-matcher.srv.ns"
    BIZPOST = "hanabi-post.srv.ns"
    BIZRECORD = "hanabi-record.srv.ns"
    BIZREVIEW = "hanabi-review.srv.ns"
    BIZCHAT = "hanabi-chatcore.srv.ns"
    BIZCHATPUSH = "hanabi-chatpush.srv.ns"
    BIZCHATSTOR = "hanabi-chatstorage.srv.ns"
    BIZMEDIASTOR = "hanabi-media-storage.srv.ns"
    BIZMEDIACONV = "hanabi-media-storage.srv.ns"


METHOD_GET = "get"
METHOD_POST = "post"


def YMD(ts):
    return time.strftime("%Y%m%d", time.localtime(ts))


def YM(ts):
    return time.strftime("%Y%m", time.localtime(ts))


def DAY(ts):
    return time.strftime("%d", time.localtime(ts))


def GetUrl(host, port, path):
    return "http://"+str(host)+":"+str(port)+"/"+str(path)


def GetConsul():
    return consul.Consul()

#def test():
#    # get local consul agent, default to 127.0.0.1:8500
#    c = consul.Consul()
#
#    # get registered named service nodes 'hanabi-bizsrv.srv.ns', filtering passing health check.
#    idx, r = c.health.service('hanabi-acnt.api.ns', passing=True)
#    for si in r:
#        print si['Service']["Address"],int(si['Service']["Port"])
#
#    # Get one and request it.
#    if len(r) == 0:
#        print "fail"
#    else:
#        addr=r[0]['Service']["Address"]
#        port=r[0]['Service']["Port"]
#        url=GetUrl(addr,port,"config/get")
#        resp=requests.post(url, json={})
#        print url, ujson.loads(resp.content)['data']['config']['partner_tid']


csl = GetConsul()
session = requests.Session()


def GetHostPort(ns):
    """
    Specify consul ns, get host/port
    """
    idx, r = csl.health.service(ns, passing=True)
    if len(r) == 0:
        return "", None
    host = r[0]['Service']['Address']
    port = r[0]['Service']["Port"]
    return host, port


def DoApi(ns, method, path, json):
    """
    if host down, ret "", "no domain"
    if up,        ret content, None
    """
    # XXX: be reusable
    host, port = GetHostPort(ns)
    if host == "" or port is None:
        return "", "no domain"
    url = GetUrl(host, port, path)
    if method == 'post':
        resp = session.post(url, json=json)
        content = resp.content
        ret = None
        try:
            ret = ujson.loads(content)
        except:
            ret = content
        finally:
            return ret, None
    elif method == "get":
        resp = session.get(url)
        content = resp.content
        ret = None
        try:
            ret = ujson.loads(content)
        except:
            ret = content
        finally:
            return ret, None


def DoApiMod(ns, method, path, json, pattern):
    """
    Wraps DoApi, cut content as pattern in jq
    """
    content, err = DoApi(ns, method, path, json)
    if err is None or len(err) == 0:
        try:
            ret = jq.all(pattern, content)
        except:
            ret = None
        finally:
            return ret
    else:
        print("%s: ns: %s, method: %s, path: %s, param: %s, cut: %s, err: %s" %
              ("ERROR", ns, method, path, ujson.dumps(json), pattern, err))
        return None


def main():
    ns = GWCOMM
    method = METHOD_POST
    path = "config/get"
    json = {}

    content = DoApiMod(ns, method, path, json,
                       '.data.config|.partner_tid, .phantom_tid')
    print content


if __name__ == "__main__":
    main()
