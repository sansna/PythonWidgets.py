#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 Apr 11 13:39:07

import time
import asyncio
import aiohttp

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


async def run(s, url, json):
    async with s.post(url, json=json) as res:
        return await res.text()


async def main():
    #url = "http://127.0.0.1:5000/"
    url = "http://api.iupvideo.net/config/get"
    st = time.time()
    async with aiohttp.ClientSession() as s:
        await run(s, url, {})
        await run(s, url, {})
        await run(s, url, {})
        await run(s, url, {})
        await run(s, url, {})
        await run(s, url, {})
        await run(s, url, {})
        await run(s, url, {})
        await run(s, url, {})
        await run(s, url, {})
        await run(s, url, {})
    et = time.time()
    print(et-st)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
