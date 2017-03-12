# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy import signals
from spiders.configs import agents
import random

class qqSpiderSpiderMiddleware(object):
	def process_request(self,request,spider):
		agent = random.choice(agents)
#		print "agent:",agent
		request.headers["User-Agent"] = agent
