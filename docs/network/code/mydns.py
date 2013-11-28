from scapy.all import *

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def send_response(x):
	req_domain = x[DNS].qd.qname
	# print req_domain
	x.show()
	res = sr1(x)
	res.show()

sniff(prn=lambda x: send_response(x), lfilter=lambda x:x.haslayer(UDP) and x.haslayer(IP) and x[IP].dst == '192.168.1.100' ) #and x.dport == 12345
