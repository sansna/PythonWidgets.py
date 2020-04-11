#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 Apr 11 15:04:33

import time
import requests
import asyncio
# Defined executors
#from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Speedup using same tcp
s = requests.Session()
#s = requests

# Wrap function for async process.
def fun():
    #url = "http://127.0.0.1:5000"
    #return s.get(url)
    url = "http://api.iupvideo.net/config/get"
    return s.post(url, "", {})


# Running async with executors/None
async def run():
    loop = asyncio.get_event_loop()

    # If need several executors, replace None with ThreadPoolExecutor/ProcessPoolExecutor
    #exe = ThreadPoolExecutor(max_workers=4)
    #exe = ProcessPoolExecutor(max_workers=5)
    futures = [
        loop.run_in_executor(
            None,
            fun
        )
        for i in range(0, 31)
    ]
    # Running 31 in concurrent, then next 31 in concurrent
    res = await asyncio.gather(*futures, *futures)

    #print([ str(i.content)+"\n" for i in res ])
    print(len(res))


def main():
    loop = asyncio.get_event_loop()
    st = time.time()
    loop.run_until_complete(run())
    et = time.time()
    print(et-st)
    loop.close()


if __name__ == "__main__":
    main()
