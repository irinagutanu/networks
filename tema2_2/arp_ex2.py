from scapy.all import *
import sys


ethernet = Ether(dst = "ff:ff:ff:ff:ff:ff")
arp = ARP(pdst = "198.13.13.0/16")
answered, unanswered = srp(ethernet / arp, timeout = 2)

print 'MAC - IP'
print answered[0][0].hwsrc
print '-',
print answered[0][0].psrc

if len(answered):
	print answered[0][1].pdst + " -- " + answered[0][1].hwdst

for answer in answered:
	print answer[1].psrc + " -- " + answer[1].hwsrc