#python制作爬虫以及控制浏览器（一）

---

前不久，接要求做个zoj的爬虫，用上了想学很久的python，然后是查博客，查语法，发现python的确是门比较简单的语言，而且由于库的支持，能做的事情非常多。
    
先讲关于爬虫，用到了库**urllib2**, **re**(正则表达式), **string**, **[beautifulsoup][1]**(十分方便的解析网页的库), **time**
[1]: http://www.crummy.com/software/BeautifulSoup/

直接上代码:


	#-*- coding: gb2312 -*-
	
	import urllib2
	from bs4 import BeautifulSoup	# 
	import re						#
	import string
	import time
	
	def geturl(url,num):
		url = url.replace(str(num),str(num+30))
		#print url
		num += 30
		return [url,num]
	
	def gettable(url):
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page)
		cansee = soup.html.body.findAll('table')[0].find('td',id = 'content').findAll('table')[0].encode('gb2312')
		return cansee
	
	if __name__ == '__main__':
		timeis = 1
		while True:	
			print timeis
			timeis += 1
			num = 0
			url = "http://acm.zju.edu.cn/onlinejudge/showRankList.do?contestId=1&from=0&order=AC"
			f = open('ranklist.html','w')
			f.write(('<html>'
						'<head>'
							'<META HTTP-EQUIV="PRAGMA" CONTENT="NO-CACHE">'
							'<META HTTP-EQUIV="EXPIRES" CONTENT="0">'
							'<title>ZOJ :: Problems :: Rank List</title>'
							'<link rel="stylesheet" href="zoj.css" type="text/css">'
						'</head>'))
	
			endpage = 4
			#get every page's 
			while num < endpage*30:
				cansee = gettable(url)
				cansee = cansee[:cansee.find('</table>')]
				if num != 0:
					cansee = cansee[cansee.find('<tr class="rowOdd">'):]
				f.write(str(cansee))
				[url, num] = geturl(url,num)
	
			f.write('</table></html>')
			f.close
	
			time.sleep(10)

用到了beautifulsoup的函数：
	
* 抓取页面：
<pre><code>page = urllib2.urlopen(url)
soup = BeautifulSoup(page)
print soup
</code></pre>

* 查找元素：
<pre><code>soup.html.body	
soup.findAll('table')[0]
soup.find('td',id = 'content')
</code></pre>

* 编码转换：
<pre><code>soup.encode('gb2312')
</code></pre>

Note:具体API查找可以到[官网doc][1]找
[1]: http://www.crummy.com/software/BeautifulSoup/bs4/doc/

安装beautifulsoup

	cd /path/to/beautifulsoup
	python setup.py build
	python setup.py install