Some NetWork Tools
=====

+ 监听和扫描：wireshark，tcpdump，nmap
+ 应用层：nc，wget，curl，w3m
+ 编程接口：libpcap/winpcap，libnids，libnet/raw sockets，snort，libnetfilter*(libipq)/divert sockets


##nmap

端口扫描工具之一

    whatever@whatever:~$ nmap -sT 61.135.169.125
    
    Starting Nmap 6.00 ( http://nmap.org ) at 2013-11-17 21:14 CST
    Nmap scan report for 61.135.169.125
    Host is up (0.029s latency).
    Not shown: 999 filtered ports
    PORT   STATE SERVICE
    80/tcp open  http
    
    Nmap done: 1 IP address (1 host up) scanned in 5.42 seconds


##w3m

在终端上的浏览器

##探索和构造工具

我们需要通过一些构造性的工具，设计特殊的包和特殊的对照试验来对GFW进行逆向工程，试图了解GFW的特性和工作机制。

**wget、curl、w3m**都是应用层的标准HTTP工具，看用户自己的喜好。不过由于wget的bug #20416，HTTP诊断所需的“下载部分内容”的功能必须靠curl -r来实现。主要用于HTTP协议及以上的探索。

**nc**是TCP/IP瑞士军刀。用脚本+nc要比走套接字五步曲(创建、绑定、监听、接收、读取)方便得多。可以用来进行应用层任意协议的研究，比如构造畸形HTTP头探查协议解析漏洞。

libnet、raw socket可以用来在网络层和传输层构造包。前者的包构造接口比较方便简单；如果希望不使用第三方库则raw(7)也可实现同样功能；如果没有TCP offload功能，可以把libnet算校验和的代码偷过来。适合做入侵检测漏洞实验。另外还可以看看libdnet。

##入侵检测工具

入侵检测简单说无非就是对报文进行更加细致的检测。前面我们通过人工看wireshark可以实现研究性的“入侵检测”，在研究定型之后要根据研究结果进行自动化的入侵检测，于是便要用到这些工具。

**libpcap/winpcap、raw socket**可以用来在网络层听包。raw(7)的好处是已经由操作系统的IP栈做好了IP包分片组装、接口规范（socket(7)、raw(7)）、可以获得原始的时间戳。Winsock的接口不太规范，觉得Winsock的文档比较糟糕，Windows下还是winpcap比较方便。

**libnids**提供了一个TCP/IP栈，需结合*pcap使用。有基本的传输层入侵检测能力，接口比较友好文档比较齐全。适合做一些轻量级的入侵检测。

snort是“业界标准”的入侵检测系统，自带仔细编写的TCP/IP栈，入侵检测功能和扩展能力都很强大，可以扩展成为入侵检测平台，可与周边的免污染DNS解析器、HTTP代理自动配置平台、本地路由配置等工具高度整合，协同对抗GFW的干扰。但是仅研究的话，由于其规则太专用化、不够通用，难以进行一般性的入侵检测实验。需要自行编写动态组件，但是这方面文档比较缺乏，耦合度很高，需要彻底研究其代码后尚能动工，难度较大。snort 3.0实现了lua脚本，功能值得期待。

**libnetfilter*(Linux)、divert sockets(FreeBSD)**可以在用户态直接操作TCP/IP栈，是进行入侵检测和响应最直接、最基于目标（target-based）、最强大的方式。内联snort（snort-inline）便基于libipq（被libnetfilter*取代）或divert sockets，进行报文丢弃、拒绝、数据修改替换等强大动作。适合在研究定型之后以其编写专门入侵防御软件来对抗GFW干扰，要比libpcap+libnet强大许多。继续往下走进内核写内核模块（网卡驱动）来做这方面的入侵防御就过于牛刀杀鸡、耦合性过高，不提了。