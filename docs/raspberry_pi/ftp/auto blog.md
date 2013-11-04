自动博客更新
====


最近用了一个轻量的博客php，配合Markdown使用————[mBlog](https://github.com/neofish/mBlog)，简约风格。

十分方便，下载，放到/var/www处解压，将markdown文件放到docs文件夹下即可。
话说CSS并不是符合自己的要求
如图，没有代码高亮，没有分割线，不能添加图片等问题，还好是开源的，所有有时间自己修改。

然后今天的话题是博客的自动更新，也就是要将本地的blog文件夹通过ftp上传服务器raspberry pi的指定文件夹下。

写了两个版本bash版和python版：

然后吐槽下bash，真的不方便。有些错误还不真不知道原因。比如
    
> 判断时 == 和 = 应该是没区别的，但是一用 == 就错

> 因为要在ftp内输入固定指令，而指令和我的文件夹有关，所以必须读一次文件就连一次ftp，效率很低

如此这些问题，如果有人会解决，那么就4个字“请联系我”。

然后还就只帖python的代码好了：
    
    # -*- coding: utf-8 -*-
    #!/usr/bin/python  
    import sys
    import os
    import ftplib
    import socket
    
    CONST_HOST = " "  # your ftp host
    CONST_USERNAME = " "      # your login name
    CONST_PWD = " "      # your password
    CONST_BUFFER_SIZE = 8192     # give a buffer size
    CONST_WORKPWD = "/home/whatever/Dropbox/blog"  # from where
    FTP_WORKPWD = "/var/www/whateverblog/docs"     # to where
    
    COLOR_NONE = "\033[m"  
    COLOR_GREEN = "\033[01;32m"  
    COLOR_RED = "\033[01;31m"  
    COLOR_YELLOW = "\033[01;33m"  
    
    #connect ftp
    def connect():
    	try:
    		ftp = ftplib.FTP(CONST_HOST)
    		ftp.login(CONST_USERNAME, CONST_PWD)
    		return ftp
    	except socket.error,socket.gaierror:  
    		print("FTP is unavailable, please check the host,username and password!")  
    	sys.exit(0)
    
    #disconnect ftp
    def disconnect(ftp):  
    	ftp.quit()
    
    # upload file
    def upload(ftp, filepath):  
    	f = open(filepath, "rb")  
    	file_name = os.path.split(filepath)[-1]  
    	try:  
    		ftp.storbinary('STOR %s'%file_name, f, CONST_BUFFER_SIZE)  
    	except ftplib.error_perm:  
    		return False  
    	return True  
    
    # dele direction
    def rmftpdir(ftp, newdir):
    	for lists in ftp.nlst(newdir):
    		# print lists
    		try:
    			ftp.cwd(os.path.join(newdir,lists))
    			rmftpdir(ftp, os.path.join(ftp,os.path.join(newdir,lists)))
    		except ftplib.error_perm:
    			ftp.delete(os.path.join(newdir,lists))
    	ftp.rmd(newdir)
    
    # bianli and upload
    def bianli(ftp, rootDir, ftpolddir):
    	for lists in os.listdir(rootDir): 
    		path = os.path.join(rootDir, lists)
    		if os.path.isdir(path): 
    			try:
    				ftp.mkd(os.path.join(ftpolddir,lists)) # if can't make the direction, mean it is already exist
    			except ftplib.error_perm:
    				rmftpdir(ftp, os.path.join(ftp,ftpolddir,lists)) 
    				ftp.mkd(os.path.join(ftpolddir,lists))
    				print(("MAKEDIR: %s "+COLOR_GREEN+"SUCCESS"+COLOR_NONE)%lists)
    			bianli(ftp, path, os.path.join(ftpolddir,lists))
    		else:
    			ftp.cwd(ftpolddir) #+ os.path.basename(path))
    			upload(ftp, path) 
    			print(("UPLOAD: %s "+COLOR_GREEN+"SUCCESS"+COLOR_NONE)%path)
    
    def main():
    	ftp = connect()
    
    	os.chdir(CONST_WORKPWD)
    	new_dir = ''
    	bianli(ftp, CONST_WORKPWD, FTP_WORKPWD)
    
    	# ftp.cwd(FTP_WORKPWD)
    	# list = ftp.nlst()       # 获得目录列表
    	# for name in list:
    	# print(name)             # 打印文件名字
    	
    	disconnect(ftp)
    
    if __name__ == "__main__":  
    	main()  