#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: user
# Date  : 2020 Jul 17 10:04:36 PM

import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
import asyncio
import websockets
import ujson
from lib.decorator.ccrt.procs import ppyrun

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

def GenReconnect():
    dic = {}
    dic.update({"id":"6810add","t":1,"sid":"141100b4128b187c","mid":1111,"d":{"data":{"from":"reconnect","is_anchor":0},"id":3,"type":1},"ts":1600289445781,"ip":"111.194.91.200"})
    return ujson.dumps(dic)

async def hello():
    uri = "wss://live.ippzone.net/ws?h_did=021e3ae93ed81d293fd9a07674f3562d_h5_game&token=xxxx&h_m=1111"
    async with websockets.connect(uri) as websocket:
        dic = GenReconnect()
        print (dic)
        await websocket.send(dic)
        greet = await websocket.recv()
        info=ujson.loads(greet)
        if info.get('t',0) == 2:
            sid = info.get('d', dict()).get('sessionid', '')
            if len(sid) > 0 :
                print (sid)
                dic=ujson.loads(dic)
                dic.update({'t':3,'sid':sid,'cid':''})
                dic=ujson.dumps(dic)
                await websocket.send(dic)
                greet = await websocket.recv()
                print(greet)

@ppyrun
def run():
    while True:
        asyncio.get_event_loop().run_until_complete(hello())

def main():
    run()
    #for i in range(1, 10):
        #run()

if __name__ == "__main__":
    main()

