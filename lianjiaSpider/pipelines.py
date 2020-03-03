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
                # 清理房屋面积数据 去掉单位
                area = re.findall(r'(\w*[0-9]+)\w*',item['area'])
                if area:
                    item['area'] = int(area[0])

                # 部分租金为区域 取其平均数
                if '-' in item['price']:
                    index = str(item['price']).index('-')
                    min_price = str(item['price'])[:index]
                    max_price = str(item['price'])[index+1:]
                    item['price'] = int((int(min_price)+int(max_price))/2)
                else:
                    item['price'] = int(item['price'])

                # 清理户型数据
                item['houseType'] = str(item['houseType']).strip().strip('\n')
                item['hall_num'] = item['houseType'][0]
                item['bedroom_num'] = item['houseType'][2]
                item['bathroom_num'] = item['houseType'][4]

                # 存入数据库
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
