from scapy.all import *

ip = IP()
ip.src = '198.13.0.15'
ip.dst = '198.13.0.14'
ip.tos = int('011110' + '11', 2)#set ECN 11 and DSCP AF33 = 011110


tcp = TCP()
tcp.sport = 54321
tcp.dport = 10000

## SYN ##
tcp.seq = 100
tcp.flags = 'S' # flag de SYN
raspuns_syn_ack = sr1(ip/tcp)

op_index = TCPOptions[1]['MSS']
op_format = TCPOptions[0][op_index]
value = struct.pack(op_format[1],2) 
tcp.options = [('MSS',value)] 

tcp.seq += 1
tcp.ack = raspuns_syn_ack.seq + 1
tcp.flags = 'EC'#setting ECE and CWR
ACK = ip / tcp
ACK = ip / tcp

send(ACK)

for char in "mcm":
    tcp.flags = 'PAEC'
    tcp.ack = raspuns_syn_ack.seq + 1
    print "Sent: " + char
    rcv = sr1(ip/tcp/char)
    rcv
    tcp.seq += 1

tcp.flags = 'R'
RES = ip/tcp
send(RES)
