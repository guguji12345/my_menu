# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem

class JdPhonePipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri = crawler.settings.get("MONGO_URI"),
            mongo_db = crawler.settings.get("MONGO_DB")
        )
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self,item,spider):
        name = item.__class__.__name__
        collection = self.db[name]
        condition = {'url':item['url']}
        result = collection.find_one(condition)
        if result:#数据去重,增量式爬取
            del result["_id"]
            if item != result:
                collection.update(result,{"$set":item})
                print("数据更新成功")
                return item
            else:
                raise DropItem("数据库中已存在该组数据")
        else:
            collection.insert(dict(item))
            print("数据入库成功")
            return item

    def close_spider(self,spider):
        self.client.close()
