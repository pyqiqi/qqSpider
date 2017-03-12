#encoding=utf-8
import scrapy
import configs
import getGTK
import os


class imageSpider(scrapy.spiders.CrawlSpider):
	name = "imageSpider"
	targetQqList = configs.targetQqList
	selfQq = configs.selfQq
	cookieStr = configs.cookieStr
	cookieDic = configs.cookieDic
	p_skey,skey,rv2 = getGTK.getKeys(cookieStr)
	gtk = getGTK.getNewGTK(p_skey,skey,rv2) 
	countPhotos = 0
	
	targetQqScrawl = set(targetQqList)
	finishQq = set()


	def start_requests(self):
		while self.targetQqList.__len__():
			targetQq = self.targetQqList.pop()
			self.finishQq.add(targetQq)
			url = "http://h5.qzone.qq.com/proxy/domain/shalist.photo.qq.com/fcgi-bin/fcg_list_album_v3?g_tk="+self.gtk+"&hostUin="+targetQq+"&uin="+self.selfQq+"&inCharset=utf-8&outCharset=utf-8"
			yield scrapy.http.Request(url=url,cookies=self.cookieDic,meta={"targetQq":targetQq},callback=self.parseAlbumList)
	

	def parseAlbumList(self,response):
		targetQq = response.meta["targetQq"]
		selfQq = self.selfQq
		gtk = self.gtk
		content = response.body #相册信息网页内容
		count = 0		#相册总数
		index = -1		#索引
		topicIdList = []	#相册的ID列表
		albumNameList = []	#相册名字列表
		totalList = [] 		#每个相册里的相片总数列表
		urlList = []		#相册的url列表
	
		#创建文件夹
		if(os.path.exists("/root/qq/") == False):
			os.mkdir("/root/qq/")
		if(os.path.exists("/root/qq/"+targetQq) == False):
			os.mkdir("/root/qq/"+targetQq)
			print "~~~~~~~~~~?????/////"

		while True:
			p = 0
			index = content.find('"id" : "',index+30)
			p = content.find('"',index+10)
			topicId = content[index+8:p]
			if index == -1:
				break
			#寻找相册名
			index_name_r = content.find('"name"',index)
			index_name_l = content.find(',',index_name_r+10) 
			name = content[index_name_r+10:index_name_l-1]
			#寻找相片数量
			index_total_r = content.find('"total"',index_name_l)
			index_total_l = content.find(',',index_total_r+8)
			total = content[index_total_r+10:index_total_l]
			#寻找相册问题的位置
			index_question_r = content.find('"pypriv" : 3',index_name_l)
			index_question_r = content.find(':',index_question_r+13)
			question = content[index_question_r-10:index_question_r-2]
	
			print "相册名",name
			print "相片总数",total
			print "相册Id",topicId
			#将所有找到的信息添加到列表中
			if((total != '0') & (question !='question')):
#				ImgListCount = ImgListCount + 1
#				topicIdList.append(topicId)
#				totalList.append(total)
#				albumNameList.append(name)
				photosPath = "/root/qq/"+targetQq+"/photos"
				if(os.path.exists(photosPath) == False):
					os.mkdir(photosPath)
				path = photosPath+name+"("+total+")"
				if(os.path.exists(path) == False):
					os.mkdir(path)
				
				url = 'http://h5.qzone.qq.com/proxy/domain/shplist.photo.qzone.qq.com/fcgi-bin/cgi_list_photo?g_tk='+gtk+'&hostUin='+targetQq+'&topicId='+topicId+'&uin='+selfQq+'&pageStart=0&pageNum='+total+'&inCharset=utf-8&outCharset=utf-8'
				
				meta = {
				"targetQq":targetQq,
				"path":path
				}
				yield scrapy.http.Request(url=url,cookies=self.cookieDic,meta=meta,callback=self.parsePhotoUrl)

	def parsePhotoUrl(self,response):
		content = response.body
		targetQq = response.meta["targetQq"]
		path = response.meta["path"] 

		index_r = 0
		index_l = 0
		count = 0
		while True:			
			index_r = content.find('"url" : "',index_r+20)
			if index_r == -1:
				break
			index_l = content.find(',',index_r+9)
			url = content[index_r+9:index_l-1]
			url = url.replace('\\','')
			url = url[:-1]
			if '=' in url:
				pass
			else:
#				print '==================URLERROR================='
#				print url
				continue

#			print url
			meta = {
			"path":path,
			"count":count
			}
			count = count + 1
			yield scrapy.http.Request(url=url,cookies=self.cookieDic,meta=meta,callback=self.downloadPhoto)
			
	def downloadPhoto(self,response):
		path = response.meta["path"]
		count = response.meta["count"]
		filePath = path +'/'+ str(count)+'.jpg'
		print "filePath:",filePath
		with open(filePath,'wb') as handle:
			handle.write(response.body)
		print ">>>>>>>>>>>>>>>>>>>>Downloaded",self.countPhotos,"photos","<<<<<<<<<<<<<<<<<<<<"
		self.countPhotos = self.countPhotos + 1
			
