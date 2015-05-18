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
import time
class BoardInfoPipeline(object):
    dbPrime = 97
    def __init__(self):
        leancloud.init('yn33vpeqrplovaaqf3r9ttjl17o7ej0ywmxv1ynu3d1c5wk8', master_key='zkw2itoe7oyyr3vmyrs8m95gbk0azmikc3jrtk2lw2z4792i')

    def process_item(self, item, spider):
        tableIndex = int(100*time.time())%self.dbPrime
        if tableIndex<10:
            tableIndexStr = '0' +str(tableIndex)
        else :
            tableIndexStr = str(tableIndex)

        boardId = re.split('/board/',item['boardLink'])[1]
        BoardInfo = Object.extend('BoardInfo')
        BoardStatus = Object.extend('BoardStatus'+tableIndexStr)
        boardInfo = BoardInfo()
        boardStatus = BoardStatus()
        query = Query(BoardInfo)

        query.equal_to('boardId',boardId)
        try:
            boardInfoRet = query.find()
        except LeanCloudError,e:
            boardInfoRet =[]
            print e
            
        if boardInfoRet:

            boardInfoRet[0].set('moderatorLinkList',item['moderatorLinkList'])
            boardInfoRet[0].set('moderatorIdList',item['moderatorIdList'])
            boardInfoRet[0].set('recordNum',item['recordNum'])
            boardInfoRet[0].set('currentOnlineNum',item['currentOnlineNum'])
            boardInfoRet[0].set('todayQuestionNum',item['todayQuestionNum'])
            boardInfoRet[0].set('totalQuestionNum',item['totalQuestionNum'])
            boardInfoRet[0].set('totalPageNum',item['totalPageNum'])
            try:
                boardInfoRet[0].save()
            except LeanCloudError,e:
                print e
        else:
            boardInfo.set('boardId',boardId)
            boardInfo.set('moderatorLinkList',item['moderatorLinkList'])
            boardInfo.set('moderatorIdList',item['moderatorIdList'])
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

        boardStatus.set('boardId',boardId)
        boardStatus.set('moderatorLinkList',item['moderatorLinkList'])
        boardStatus.set('moderatorIdList',item['moderatorIdList'])
        boardStatus.set('recordNum',item['recordNum'])
        boardStatus.set('recordTime',item['recordTime'])
        boardStatus.set('currentOnlineNum',item['currentOnlineNum'])
        boardStatus.set('todayQuestionNum',item['todayQuestionNum'])
        boardStatus.set('totalQuestionNum',item['totalQuestionNum'])
        boardStatus.set('totalPageNum',item['totalPageNum'])

        try:
            boardInfo.save()
        except LeanCloudError,e:
            print e


        #return item
        DropItem()


