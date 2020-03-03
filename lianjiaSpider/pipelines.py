# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from lianjiaSpider import settings
from .item.zufang import zufangItem
import re
from lianjiaSpider.zone.city import cities
import math


class LianjiaspiderPipeline(object):
    def __init__(self,host,port,zufang_db):
        self.host = host
        self.port = port
        self.db_name = zufang_db
        # 链接数据库
        client = pymongo.MongoClient(host=self.host,port=self.port)
        self.tdb = client[self.db_name]
        #self.post = self.tdb[post]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host = crawler.settings.get('MONGODB_HOST'),
            port = crawler.settings.get('MONGODB_PORT'),
            zufang_db = crawler.settings.get('MONGODB_DBNAME'),
            #post = crawler.settings.get('MONGODB_DOCNAME'),


        )

    def process_item(self, item, spider):
        if isinstance(item, zufangItem):
            try:
                area = re.findall(r'(\w*[0-9]+)\w*',item['area'])
                if area:
                    item['area'] = int(area[0])
                if '-' in item['price']:
                    index = str(item['price']).index('-')
                    min = str(item['price'])[:index]
                    max = str(item['price'])[index+1:]
                    item['price'] = math.floor((int(min)+int(max))/2)
                else:
                    item['price']=int(item['price'])
                item['houseType'] = str(item['houseType']).strip().strip('\n')
                info = dict(item)
                doc_name = "zufang_"+(cities[item['city']])
                self.post = self.tdb[doc_name]
                if self.post.insert(info):
                    print('成功插入一条数据')
                else:
                    print('插入数据失败')
                    print(info)
            except Exception as e:
                print(e)
                pass
        return item
