# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class moodSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    	moodContent = scrapy.Field()
	commentPeoples = scrapy.Field()
	commentNum = scrapy.Field()
	parsePeoples = scrapy.Field()
	parseNum = scrapy.Field()
	createTime = scrapy.Field()

