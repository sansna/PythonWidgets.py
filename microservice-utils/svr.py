#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 May 16 18:00:31

import time
import consul
import sys
from svd import GetUrl

now = int(time.time())
today = int(now+8*3600)/86400*86400-8*3600
dayts = 86400
hourts = 3600
mints = 60
yesterday = today - dayts

def YMD(ts):
    return time.strftime("%Y%m%d", time.localtime(ts))

def YM(ts):
    return time.strftime("%Y%m", time.localtime(ts))

def DAY(ts):
    return time.strftime("%d", time.localtime(ts))

def CslReg(csl, name, host, port, check=None):
    while True:
        try:
            # https://www.consul.io/api-docs/agent/check
            if check is None:
                ck = consul.Check.tcp(host,port,"1s",timeout="10s")
            else:
                ck = check
            csl.agent.service.register(name, address=host, port=port, check=ck)
            break
        except:
            print ("err. retrying...: ", sys.exc_info())
            time.sleep(0.5)

# XXX: 1. start consul by consul agent -dev
# 2. register a service with following scripts
# 3. start a server at speified host/port
# 4. svd to call api from other places
def main():
    c = consul.Consul()
    svcname = "my_host"
    listenhost = "127.0.0.1"
    listenport = 6500
    urlhello = GetUrl(listenhost, listenport, "hello")

    CslReg(c, svcname, listenhost, listenport, check=consul.Check.http(urlhello, interval='3s'))
    #CslReg(c, "my_host", "127.0.0.1", 6500)
    #time.sleep(100)

if __name__ == "__main__":
    main()

