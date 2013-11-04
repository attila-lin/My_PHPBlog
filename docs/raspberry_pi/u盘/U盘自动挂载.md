#U盘的自动挂载

###1.在使用busybox制作根文件系统的时候，选择支持mdev

    Linux System Utilities  --->   
               [*] mdev      
               [*] Support /etc/mdev.conf
               [*] Support command execution at device      
    addition/removal

###2.在文件系统添加如下内容

    Vim /etc/init.d/rcS
    
    mount -t tmpfs mdev /dev 
    mount -t sysfs sysfs /sys
    mkdir /dev/pts
    mount -t devpts devpts /dev/pts

echo /sbin/mdev>/proc/sys/kernel/hotplug
        mdev –s

这些语句的添加在mdev的手册中可以找到。

###3.添加对热插拔事件的响应，实现U盘和SD卡的自动挂载。

        
    Vim /etc/mdev.conf

    mmcblk[0-9]p[0-9] 0:0 666 @ /etc/usb/sd_card_inserting
    mmcblk[0-9] 0:0 666 $ /etc/usb/sd_card_removing
    sd[a-z] [0-9] 0:0 666 @ /etc/usb/usb_inserting
    sd[a-z] 0:0 666 $ /etc/usb/usb_removing

红色部分，是一个脚本，脚本内容可以根据我们的需要定制，可以实现挂载，卸载或其他一些功能。

如下是自动挂载和卸载的脚本：
    
**/etc/sd_card_inserting**

    #!/bin/sh
    mount -t vfat /dev/mmcblk0p1 /mnt/sd
    
**/etc/sd_card_removing**

    #!/bin/sh
    sync
    umount /mnt/sd
        
udisk相似

然后加+x:

    chmod u+x mmc*
    chmod u+x usb*