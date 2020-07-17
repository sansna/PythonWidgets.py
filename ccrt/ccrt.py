#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 Apr 07 09:37:31

import time
from requests import post
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

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

def wrap_post(url, dic):
    print post(url, json=dic).content

def post_api(urls):
    with ThreadPoolExecutor(max_workers=5) as exe:
        exe.map(wrap_post, urls, repeat(dict()), timeout=5)

def main():
    urls = 10*["http://api.iupvideo.net/config/get","http://api.iupvideo.net/config/get","http://api.iupvideo.net/config/get","http://api.iupvideo.net/config/get","http://api.iupvideo.net/config/get"]
    post_api(urls)

if __name__ == "__main__":
    main()

