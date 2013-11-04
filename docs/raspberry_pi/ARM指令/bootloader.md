bootloader
====

David Welch的GitHub的 bootloader05给出了一个非常简单的RPi bootloader，他的代码链接在内存的0x00020000位置，一直在监听串口是 否有XMODEM协议的文件下载，如果有就开始接收数据，并复制到0x00008000位置，传输完成后跳转到 0x00008000去执行。

python xmodem-loader.py -p com3 -baud 115200 output.bin
你的任务是修改bootloader和python脚本实现如下功能：

调用命令 
    python xmodem-loader.py -p com3 -baud 115200 
启动脚本并且与板卡建立串口连接，之后可以发送下面的命令。

+ load *.bin 下载程序*.bin

+ go 执行已下载的程序

+ peek addr 以一个字为单位读取内存中addr位置的数据（addr是4字节对齐，十六进行的形式，长度为8，例如 0x00008000），并以十六进制的形式输出

+ poke addr data 以一个字为单位修改内存中addr位置的数据为data（addr是4字节对齐，十六进行的形式，长 度为8， data也是十六进行的形式，长度为8）
+ verify *.bin 验证已下载的程序和*.bin是否完全相同。





