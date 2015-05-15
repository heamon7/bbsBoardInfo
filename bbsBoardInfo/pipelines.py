# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import leancloud
from leancloud import Object
from leancloud import LeanCloudError
from leancloud import Query
from scrapy import log
from scrapy.exceptions import DropItem

class BoardInfoPipeline(object):
    def __init__(self):
        leancloud.init('mctfj249nwy7c1ymu3cps56lof26s17hevwq4jjqeqoloaey', master_key='ao6h5oezem93tumlalxggg039qehcbl3x3u8ofo7crw7atok')

    def process_item(self, item, spider):
        BoardInfo = Object.extend('BoardInfo')
	boardInfo = BoardInfo()
        boardInfo.set('boardLink',item['boardLink'])
        for index , people in enumerate(item['moderatorLinkList']):
            boardInfo.set('moderatorLink'+str(index),item['moderatorLinkList'][index])
            boardInfo.set('moderatorId'+str(index),item['moderatorIdList'][index])

        boardInfo.set('recordNum',item['recordNum'])
        boardInfo.set('recordTime',item['recordTime'])
        boardInfo.set('currentOnlineNum',item['currentOnlineNum'])
        boardInfo.set('todayQuestionNum',item['todayQuestionNum'])
        boardInfo.set('totalQuestionNum',item['totalQuestionNum'])
        boardInfo.set('totalPageNum',item['totalPageNum'])

        try:
            boardInfo.save()
        except LeanCloudError,e:
            print e


        return item
        #DropItem()


