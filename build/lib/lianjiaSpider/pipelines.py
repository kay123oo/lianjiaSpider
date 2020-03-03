# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from lianjiaSpider import settings
from .item.zufang import zufangItem



class LianjiaspiderPipeline(object):
    def __init__(self,host,port,zufang_db,post):
        self.host = host
        self.port = port
        self.db_name = zufang_db
        # 链接数据库
        client = pymongo.MongoClient(host=self.host,port=self.port)
        self.tdb = client[self.db_name]
        self.post = self.tdb[post]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host = crawler.settings.get('MONGODB_HOST'),
            port = crawler.settings.get('MONGODB_PORT'),
            zufang_db = crawler.settings.get('MONGODB_DBNAME'),
            post = crawler.settings.get('MONGODB_DOCNAME'),


        )

    def process_item(self, item, spider):
        print("isinstance(item, zufangItem):")
        print(isinstance(item, zufangItem))
        if isinstance(item, zufangItem):
            try:
                if '公寓' in item['title']:
                    item['houseType'] = '公寓'
                else:
                     item['houseType'] = '个人房源'
                     item['rentType'] = item['title'][0:2]
                info = dict(item)
                if self.post.insert(info):
                    print('成功插入一条数据')
                else:
                    print('插入数据失败')
                    print(info)
            except Exception as e:
                print(e)
                pass
        return item
