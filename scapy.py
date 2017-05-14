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

# Self construct packet and send
a=IP(dst="10.0.2.2",src="10.0.2.3",ttl=10)
b=Ether(dst="00:00:00:00:00:01")
sendp(b/a,iface="ens2f0")
