# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import datatime

class Test1Pipeline(object):

    def __init__(self):
        Client = MongoClient("mongodb://haoduofuli:haoduofuli123@localhost:27017/haoduofuli")#这个字符串有问题，等我搞清楚了pymongo了再回来改
        db = Client['radiowave']
        self.save = db['radiowave']
    def process_item(self, item, spider):
        if isinstance(item, RadiowaveItem):
            dramaid = item['dramaid']
            dramaname = item['dramaname']
            category = item['category']
            imgurl = item['imgurl']
            dramaurl = item['dramaurl']
            ip = item['ip']
            post = {
                '下载链接': dramaurl,
                '片名':dramaname,
                '种类':category,
                '海报':imgurl,
                '编号':dramaid,
                '执行任务的服务器':ip,
                '储存时间': datetime.datetime.now()
            }
            self.save.insert_one(post)

        return item
