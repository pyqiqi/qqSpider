#encoding=utf-8
import scrapy
import json
import configs
import getGTK
import os
import time

class moodSpider(scrapy.spiders.CrawlSpider):
	name = "moodSpider"
	targetQqList = configs.targetQqList
	selfQq = configs.selfQq
	cookieStr = configs.cookieStr
	cookieDic = configs.cookieDic
	p_skey,skey,rv2 = getGTK.getKeys(cookieStr)
	gtk = getGTK.getNewGTK(p_skey,skey,rv2)

	endFlag = 0
	msgNum = 0
	targetQqScrawl = set(targetQqList)

	def start_requests(self):
		while self.targetQqList.__len__():
			targetQq = self.targetQqList.pop()
			self.endFlag = 1
			print "----------------------"
			index = 10000
			url = "https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin="+targetQq+"&pos="+str(index)+"&num=20&g_tk="+self.gtk
			meta ={
			"targetQq":targetQq	
			}
			yield scrapy.http.Request(url=url,cookies=self.cookieDic,meta=meta,callback=self.parseMsgNum)

	def parseMsgNum(self,response):
		content = response.body
		targetQq = response.meta["targetQq"]
		msgnumIndexl = content.rfind("msgnum")+8
		msgnumStr = content[msgnumIndexl:msgnumIndexl+10]
		msgnumIndexr = msgnumStr.find(',')
		print "msgnumStr>>>>>>>>>>",msgnumStr
		msgNum = int(msgnumStr[0:msgnumIndexr])
		print "msgnum>>>>>>>>>>",msgNum
		index = 0
		while(index < msgNum):
			url = "https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin="+targetQq+"&pos="+str(index)+"&num=20&g_tk="+self.gtk
			meta = {
			"targetQq":targetQq
			}
			yield scrapy.http.Request(url=url,cookies=self.cookieDic,meta=meta,callback=self.parseMood)
			index = index + 20


	def parseMood(self,response):
		targetQq = response.meta["targetQq"]
		content = response.body
		content = content.replace("null","0")
		content = eval(content[content.find('[')+1:content.rfind(']')])
		for contentDic in content:
			for key in contentDic:
				if (key == "content"):
					print key,"=>",contentDic[key],"time:",contentDic["createTime"]
					unikey =  "http://user.qzone.qq.com/"+targetQq+"/mood/"+contentDic["tid"]
					url = "https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/user/qz_opcnt2?_stp=&unikey="+unikey+"&g_tk="+self.gtk
					meta = {
					"targetQq":targetQq
					}
					yield scrapy.http.Request(url=url,cookies=self.cookieDic,meta=meta,callback=self.parsePraise)

	def parsePraise(self,response):
		targetQq = response.meta["targetQq"]
		content = response.body
		content = content[content.find("cnt:"):]
		parseNum = int(content[4:content.find(",")])
		print "parseNum:",parseNum
		content = content[content.find("[[")+2:content.find("]]")-3]
		print "list:",content
		if(parseNum == 0):
			pass
		elif(parseNum == 1):
			person = content
			print "person list:",person
		elif(parseNum > 2):
			persons = content.split('",0],[')
			for person in persons:
				print "person list:",person


