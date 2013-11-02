# python制作爬虫以及控制浏览器（二）

---

在上一篇讲到了如何使用python抓取网页以及Beautifulsoup的相关用法，这章我想讲如何通过控制实际浏览器来操作页面的。

通过搜集相关资料，我先是用了pamie这个开源库，是针对IE8以下版本做的，然后发现了selenium，发现有了更多的选择，可以控制Chrome，ff等浏览器。

那先讲pamie。

## pamie

可以在 https://sourceforge.net/projects/pamie/ 下载到

pam30是针对python3的，只是测试版本，所以建议用最新版本的cpamie2

* 环境 :

	* 浏览器：ie8（经测试，ie9不能用）

	* 库：cpamie2

	* python version：python 2.7

**Note:** 
	
	如何卸载IE9：	
	win7默认IE8,到控制面板 -> 程序 -> 程序和功能 -> 已安装更新,找到IE9的更新，然后卸载,
	重启后，IE就变成IE8了


pamie安装就不赘述了，拷入'C:\Python27\Lib\site-packages'

然后是代码：

	# coding=utf-8
	import cPAMIE
	import cReport
	import cModalPopUp
	import winGuiAuto
	import time
	import os, sys
	
	# Initialize our stuff.
	ie = cPAMIE.PAMIE()
	rep = cReport.Report()
	wga = winGuiAuto
	
	#rep.initialize() # report初始化
	
	ie.frameName = None
	url = 'http://www.nexushd.org/details.php?id='
	
	def saythanks(begin,ends):
		for i in range(begin,ends+1):
			geturl = url + str(i)
			ie.navigate(geturl)
			time.sleep(5)
			ie.buttonClick("saythanks")
	
	if __name__ == '__main__':
		begin = raw_input( "begin:")
		ends = raw_input("ends:")
		saythanks(int(begin),int(ends))
	
	#rep.finalize()

pamie速度比较慢，但是自动保存IE的状态，不是像selenium一样初始化一个新的浏览器。所以，你可以先登录NHD，然后直接开始saythanks了

## selenium

可以在 https://pypi.python.org/pypi/selenium 下载到

代码：


	# -*- coding: gb2312 -*-
	from selenium import webdriver
	# https://pypi.python.org/pypi/selenium
	from selenium.common.exceptions import NoSuchElementException
	from selenium.webdriver.common.keys import Keys
	import time
	
	browser = webdriver.Firefox() # Get local session of firefox
	url = 'http://www.nexushd.org/details.php?id='
	loginurl = 'http://www.nexushd.org/login.php'
	
	
	def logins(names,passwd):
		browser.get(loginurl)
		elem = browser.find_element_by_name("username") # Find the query box
		elem.send_keys(names)
		elem = browser.find_element_by_name("password") # Find the query box
		elem.send_keys(passwd + Keys.RETURN)
		time.sleep(0.2) # Let the page load, will be added to the API
	
	
	def saythanks(begin,ends):
		for i in range(begin,ends+1):
			geturl = url + str(i)
			browser.get(geturl) # Load page
			try:
				elem = browser.find_element_by_id("saythanks")
				elem.click()
			except NoSuchElementException:
				continue
			time.sleep(2) #刷新时间2s
	
	def main():
		names = raw_input( "neme:")
		password = raw_input("password:")
		logins(names,password)
		begin = raw_input( "begin:")
		ends = raw_input("ends:")
		saythanks(int(begin),int(ends))
		browser.close()

	if __name__ == '__main__':
		main()

像前面说的一样，selenium是初始化一个新的浏览器，所以不包含以前的cookie，需要手动登录，但是手动登录也很简单，用到一些函数就行：
	
* elem.send_keys()
* elem.send_keys(passwd + Keys.RETURN) # 这个 Keys.RETURN 是提交

由于nhd上有些种子被删，可能出现ID不连续，加入抛出异常

	try:
		elem = browser.find_element_by_id("saythanks")
		elem.click()
	except NoSuchElementException:
		continue

## py2exe

为了让windows用户可以方便使用，使用py2exe发布，简单的说是将.py转成.exe，然后可以直接运行。

+ 第一步：安装py2exe

	* 下载地址：https://sourceforge.net/projects/py2exe/files/
	* 下载并安装

+ 第二步：编写mysetup.py

根据模版编写：
	
	# mysetup.py
	from distutils.core import setup
	import py2exe
	
	setup(
	    console=["saythanks_ff.py"],
	    options={
	            "py2exe":{
	                    "skip_archive": True,
	                    "unbuffered": True,
	                    "optimize": 2
	            }
	    }
	)


运行
	
	python mysetup.py py2exe