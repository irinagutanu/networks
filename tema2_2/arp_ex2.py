from scapy import all

ethernet = Ether(dst = "ff:ff:ff:ff:ff:ff")
arp = ARP(pdst = "198.13.13.0/16")
answered = srp1(ethernet / arp)

print 'MAC - IP'
print answered[0][0].hwsrc
print '-',
print answered[0][0].psrc

if len(answered):
	print answered[0][1].pdst + " -- " + answered[0][1].hwdst

for answer in answered:
	print answered[1].psrc + " -- " + answered[1].hwsrc