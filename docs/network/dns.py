#coding:utf-8
from scapy.all import *

sr1(IP(src="192.168.1.100",dst="8.8.8.8")/UDP()/DNS(rd=1,qd=DNSQR(qname="www.baidu.com")))
