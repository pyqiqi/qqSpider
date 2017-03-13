#encoding=utf-8
import scrapy
import json
import configs
import getGTK
import os
import time
from qqSpider.items import moodSpiderItem

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
			#print "===>>>",url
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
		#print content
		for contentDic in content:
			for key in contentDic:
				commentPeoples = []
				commentNum = 0
				#print key,"====>",contentDic[key]
				#每条心情的内容，评论，评论人
				if (key == "content"):
					moodContent = contentDic["content"]
					createTime = str(contentDic["createTime"])
					print key,"=>",moodContent,"time:",createTime
					try:
						for commentListDic in contentDic["commentlist"]:
							if(commentListDic["uin"] != self.selfQq):
								commentPeoples.append(commentListDic["uin"])
					except Exception,e:
						pass

					if (commentPeoples != []):
						for commentPeople in commentPeoples:
							commentNum = commentNum + 1

					unikey =  "http://user.qzone.qq.com/"+targetQq+"/mood/"+contentDic["tid"]
					url = "https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/user/qz_opcnt2?_stp=&unikey="+unikey+"&g_tk="+self.gtk
					meta = {
					"targetQq":targetQq,
					"moodContent":moodContent,
					"createTime":createTime,
					"commentPeoples":commentPeoples,
					"commentNum":commentNum
					}
					yield scrapy.http.Request(url=url,cookies=self.cookieDic,meta=meta,callback=self.parsePraise)

	def parsePraise(self,response):
		targetQq = response.meta["targetQq"]
		moodContent = response.meta["moodContent"]
		createTime = response.meta["createTime"]
		commentPeoples = response.meta["commentPeoples"]
		commentNum = response.meta["commentNum"]
		content = response.body
		content = content[content.find("cnt:"):]
		parseNum = int(content[4:content.find(",")])
		parsePeoplesTemp = []
		parsePeoples = []
		content = content[content.find("[[")+2:content.find("]]")-3]
		#print "list:",content
		if(parseNum == 0):
			pass
		elif(parseNum > 0):
			try:
				parsePeoplesTemp = content.split('",0],[')
			except Exception,e:
				pass
				
		#	parsePeoples = content
			for parsePeople in parsePeoplesTemp:
				parsePeoples.append(parsePeople.split(',"')[0])

		print "moodContent	==>>",moodContent
		print "commentPeoples	==>>",commentPeoples
		print "commentNum	==>>",commentNum
		print "parsePeoples	==>>",parsePeoples
		print "parseNum 	==>>",parseNum
		print "createTime	==>>",createTime

		item = moodSpiderItem()
		item["moodContent"] = moodContent
		item["commentPeoples"] = commentPeoples
		item["commentNum"] = commentNum
		item["parsePeoples"] = parsePeoples
		item["parseNum"] = parseNum
		item["createTime"] = createTime

		yield item


