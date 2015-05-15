# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BbsboardinfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    boardLink = scrapy.Field()
    moderatorLinkList = scrapy.Field()
    moderatorIdList = scrapy.Field()
    recordNum = scrapy.Field()
    recordTime = scrapy.Field()
    currentOnlineNum = scrapy.Field()
    todayQuestionNum = scrapy.Field()
    totalQuestionNum = scrapy.Field()
    totalPageNum = scrapy.Field()

