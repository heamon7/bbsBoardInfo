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


class BoardinfoerSpider(scrapy.Spider):
    name = "boardInfoer"
    allowed_domains = ["bbs.byr.cn"]
    start_urls = (
        'http://www.bbs.byr.cn/',
    )
    baseUrl = 'http://bbs.byr.cn'
    def __init__(self):
        leancloud.init('mctfj249nwy7c1ymu3cps56lof26s17hevwq4jjqeqoloaey', master_key='ao6h5oezem93tumlalxggg039qehcbl3x3u8ofo7crw7atok')

        Boards = Object.extend('Boards')
        query = Query(Boards)
        query.exists('boardLink')
        query.select('boardLink')
	query.limit(500)
        boards= query.find()
        self.urls = []
        for board in boards:
            self.urls.append(self.baseUrl+board.get('boardLink'))

    def start_requests(self):
        print "start_requests ing ......"
        print self.urls
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
