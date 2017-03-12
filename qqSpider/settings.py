# -*- coding: utf-8 -*-

BOT_NAME = 'qqSpider'

SPIDER_MODULES = ['qqSpider.spiders']
NEWSPIDER_MODULE = 'qqSpider.spiders'
DOWNLOADER_MIDDLEWARES = {
	"qqSpider.middlewares.qqSpiderSpiderMiddleware": 401,
}

#ITEM_PIPELINES = {
#	    'qqSpider.pipelines.QqspiderPipeline': 300,
#}
#IMAGES_STORE = '.'

DOWNLOAD_DELAY = 2  # 间隔时间
CONCURRENT_REQUESTS = 1

