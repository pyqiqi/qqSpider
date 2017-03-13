# -*- coding: utf-8 -*-

BOT_NAME = 'qqSpider'

SPIDER_MODULES = ['qqSpider.spiders']
NEWSPIDER_MODULE = 'qqSpider.spiders'
DOWNLOADER_MIDDLEWARES = {
	"qqSpider.middlewares.qqSpiderSpiderMiddleware": 401,
}

ITEM_PIPELINES = {
	    'qqSpider.pipelines.qqMoodsPipeline': 300,
}
#IMAGES_STORE = '.'

#间隔时间
DOWNLOAD_DELAY = 1  
#爬虫线程数
CONCURRENT_REQUESTS = 10 
#MongoDB配置
MONGODB_HOST = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_DBNAME = "qqSpiderDB"
MONGODB_DOCNAME = "qqMoods"




