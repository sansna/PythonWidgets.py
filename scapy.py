#!/usr/bin/python2

from scapy.all import * # Changing from scapy to scapy.all
# Ways to get Doc of scapy lib.
help(scapy)
help(scapy.all)
help(scapy.sendrecv)

pkts=sniff(count=1,filter="arp")
arppkt=eval(pkts[0].command())
# ls(Ether) # Show args of array Ether..
arppkt[Ether].dst="68:05:ca:3f:6d:e1"
# ls(ARP) # Show args of array ARP..
arppkt[ARP].op=2 #Reply, 1 if request
arppkt[hwdst]="68:05:ca:3f:6d:e1"
ifaces
#send(arppkt,iface="ens2f0") #In windows, using send(), seems in linux, send()
#+ do not have arg iface.. It said send() is used to send layer 3 pkts. and
#+ sendp is used to send layer 2 pkts.
sendp(arppkt,iface="ens2f0") #In linux, using sendp()..

# Test empty packet sending
sendp(Ether()/IP(),iface="ens2f0")

# Self construct IP packet and send
b=Ether(dst="00:0c:29:17:06:8e",src="00:50:56:37:28:b9",type=0x0800)
a=IP(dst="10.0.2.2",src="10.0.2.3",ttl=10)
sendp(b/a,iface="eno50336512")
# Send 80 len IP pkt, Eth/IP len = 34 Byte
sendp(b/a/Raw(RandString(size=46)),iface="eno50336512")
