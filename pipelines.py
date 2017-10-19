# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import datetime

class Test1Pipeline(object):

    def __init__(self):
        Client = MongoClient("mongodb://hmq:118667@localhost:27017/")
        db = Client['radiowave']
        self.save = db['drama']

    def process_item(self, item, spider):
        dramaid = int(item['dramaid'])
        dramaname = item['dramaname']
        category = item['category']
        imgurl = item['imgurl']
        dramapage = item['dramapage']
        post = {
            '_id': dramaid,
            '剧名': dramaname,
            '类型': category,
            '海报链接': imgurl,
            '详情页面': dramapage,
            '储存时间': datetime.datetime.now()
        }
        self.save.insert_one(post)
        return item
