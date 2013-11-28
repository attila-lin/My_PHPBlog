from scapy.all import *
import time


e = Ether()
test = IP(dst="www.baidu.com")/ICMP()
# p = sr1(e/test)
# p.show()
while True:
	sendp(e/test)
	time.sleep(1)

del(p[IP].chksum)
del(p[ICMP].chksum)

p[IP].dst = '192.168.1.103'
p[IP].src = '192.168.1.1'
p[ICMP].type = 3
p[ICMP].code = 1

e = Ether(dst="f8:a4:5f:85:4e:ed", src="f0:eb:d0:0b:11:48")

p = e/p

p.show()

# m = IP(dst="192.168.1.101",src="192.168.1.1")/ICMP(type=3,code=0)


# while True:
# 	sendp(p)
# 	time.sleep(1)