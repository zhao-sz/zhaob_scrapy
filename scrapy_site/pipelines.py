# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from scrapy_site.common.consts import const
from scrapy_site.utils import date

class ScrapySitePipeline(object):
    def process_item(self, item, spider):
        return item


class SavePipeline(object):
    initCount = 0

    def __init__(self):
        dispatcher.connect(self.spider_opended, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        dispatcher.connect(self.engine_stopped, signals.engine_stopped)
        dispatcher.connect(self.engine_started, signals.engine_started)

        # 获取当前目录，当前目录为scrapy_site项目的根目录
        self.curpath = os.getcwd()
        #爬虫爬取的数据存储文件目录
        self.spidername_filepath = self.curpath + "/scrapy_site/msg/"

        # 从配置文件keyword.conf获取关键字字典值
        self.keywordsDict = dict()
        self.getKeywords()

        #从配置文件中读取网站名称
        self.webnamesDict = dict()
        self.getWebnames()

        # 爬取信息
        self.msgDict = dict()

        SavePipeline.initCount = SavePipeline.initCount + 1

    def engine_started(self):
        pass

    def engine_stopped(self):
        print('Pipeline共初始化的次数========%s' % SavePipeline.initCount)

    def spider_opended(self, spider):
        file = open(self.spidername_filepath + spider.name, 'w')
        file.write('---')
        file.write("网站名称:" + self.webnamesDict[spider.name])
        file.write('---')
        file.write('\n')
        file.close()

    def spider_closed(self, spider):
        file = open(self.spidername_filepath + spider.name, 'a')
        print("@@@@@@@@@@@@@ spider close name is ", spider.name)
        #将爬取信息写入爬虫文件中
        if self.msgDict:
            msg = self.msgDict.get(spider.name)
            if msg:
                message = msg['msg']
                print("spider_opended=" + spider.name)
                print("**********************************************************************************************")
                print("\n")
                print(message)
                print("\n")
                print("**********************************************************************************************")
                file.write(message)
        file.close()

    def process_item(self, item, spider):
        if not item['pubtime'] or not item['title']:
            return item
        # 去除换行与空格及[]
        pubtime = item['pubtime']
        title = item['title'].encode(const.ENCODE)
        print("!!!!!! pubtime , title  name  curdate", pubtime, title.decode(), spider.name, date.get_curdate())

        if self.checkTilte(self.keywordsDict.get(spider.name), title) and date.get_curdate() == pubtime:
            msgArr = self.msgDict.get(spider.name)
            if msgArr is None:
                print("!!!!!!!@@@@@ msg is null")
                msgArr = {}
                msgArr['id'] = 0
                msgArr['msg'] = ""
            # 根据链接判断是否爬取到重复内容
            if item['link'] in msgArr['msg']:
                pass
            else:
                msgArr['id'] += 1
                msgArr['msg'] += str(msgArr['id'])
                msgArr['msg'] += '---'
                msgArr['msg'] += item['title']
                msgArr['msg'] += '---'
                msgArr['msg'] += item['link']
                msgArr['msg'] += '\n'

            print("==================添加内容====================msgArr['msg']={}".format(msgArr['msg']))
            self.msgDict.setdefault(spider.name, msgArr)
        return item


    def checkTilte(self, keywordStr, title):
        ukeywords = ['云南', '云海']
        title = title.decode()
        for uk in ukeywords:
            title = title.replace(uk, '')

        keywords = keywordStr.split(",")
        return len([True for k in keywords if k in title]) > 0

    def getKeywords(self):
        # 从配置文件中读取关键字
        fk = open(self.curpath + "/scrapy_site/" + const.KEYWORD_CONF, 'rb')
        while True:
            line = fk.readline().strip()
            line = line.decode()
            if line:
                config = line.split('===')
                self.keywordsDict.setdefault(config[0], config[1])
            else:
                break
        fk.close()

    def getWebnames(self):
        # 从配置文件中读取关键字
        fw = open(self.curpath + "/scrapy_site/" + const.WEBNAME_CONF, 'rb')
        while True:
            line = fw.readline().strip()
            line = line.decode()
            if line:
                config = line.split('===')
                self.webnamesDict.setdefault(config[0], config[1])
            else:
                break
        fw.close()