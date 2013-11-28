from scapy.all import *
import time

def resend(x):
	# x.show()
	x[Ether].dst = "f0:eb:d0:0b:11:48"
	# x[IP].dst = "192.168.1.1"
	# del(x[IP])
	sendp(x)


# not contains arp and 
sniff(iface="wlan0", filter=" host 192.168.1.101 ", prn=lambda x: resend(x))