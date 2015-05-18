# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
from scrapy.http import Request,FormRequest

import re
import leancloud
from leancloud import Object
from leancloud import LeanCloudError
from leancloud import Query
from scrapy import log
from scrapy.exceptions import DropItem

from  bbsBoardInfo.items import BbsboardinfoItem
import os


class BoardinfoerSpider(scrapy.Spider):
    name = "boardInfoer"
    allowed_domains = ["bbs.byr.cn"]
    start_urls = (
        'http://www.bbs.byr.cn/',
    )
    baseUrl = 'http://bbs.byr.cn'
    def __init__(self,stats):
        self.stats = stats
        leancloud.init('yn33vpeqrplovaaqf3r9ttjl17o7ej0ywmxv1ynu3d1c5wk8', master_key='zkw2itoe7oyyr3vmyrs8m95gbk0azmikc3jrtk2lw2z4792i')

        Boards = Object.extend('Boards')
        query = Query(Boards)
        query.exists('boardLink')
        query.select('boardLink')
        query.limit(500)
        boards= query.find()
        self.urls = []
        for board in boards:
            self.urls.append(self.baseUrl+board.get('boardLink'))
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def start_requests(self):
        #print "start_requests ing ......"
        #print self.urls
        for url in self.urls:
            yield Request(url,callback = self.parse)

    def parse(self, response):

        item = BbsboardinfoItem()
      #  inspect_response(response,self)
        item['boardLink'] = re.split('http://bbs.byr.cn(\w*)',response.url)[2]
        item['moderatorLinkList'] = response.xpath('//div[@class="b-head corner"]/span[@class="n-right"]/a/@href').extract()
        item['moderatorIdList'] = response.xpath('//div[@class="b-head corner"]/span[@class="n-right"]/a/text()').extract()
        item['recordNum'] = int(response.xpath('//div[@class="b-head corner"]/span[@class="n-left"]/span[@title]/text()').re('\d*')[3])
        item['recordTime'] = response.xpath('//div[@class="b-head corner"]/span[@class="n-left"]/span[@title]/@title').re('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
        item['currentOnlineNum'] = int(response.xpath('//div[@class="b-head corner"]/span[@class="n-left"]/text()')[0].re('\d*')[6])
        item['todayQuestionNum'] = int(response.xpath('//div[@class="b-head corner"]/span[@class="n-left"]/text()')[1].re('\d*')[5])
#	inspect_response(response,self)
        item['totalQuestionNum'] = int(response.xpath('//div[@class="t-pre-bottom"]//li[@class="page-pre"]/i/text()').extract()[0])
        try:
            item['totalPageNum'] = int(response.xpath('//div[@class="t-pre-bottom"]//ul[@class="pagination"]//ol[@class="page-main"]/li[last()-1]/a/text()').extract()[0])
        except IndexError,e:
           item['totalPageNum'] = int(response.xpath('//div[@class="t-pre-bottom"]//ul[@class="pagination"]//ol[@class="page-main"]/li[last()]/a/text()').extract()[0])
      #  print item['sectionListLink']

        return item
    def closed(self,reason):
        #f = open('../../nohup.out')
        #print f.read()
        try:
            nohupOut = open(os.getcwd()+'/nohup.out','r').read()
        except:
            nohupOut = "Cannot read nohup.out file"
        CrawlerLog = Object.extend('CrawlerLog')
        crawlerLog = CrawlerLog()

        crawlerLog.set('crawlerName',self.name)
        crawlerLog.set('crawlerLog',nohupOut)
        crawlerLog.set('closedReason',reason)
        crawlerLog.set('crawlerStats',self.stats.get_stats())
        try:
            crawlerLog.save()
        except:
            pass
