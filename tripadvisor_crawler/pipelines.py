# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo

class MongoPipeline(object):

    def open_spider(self, spider):
        self.collection_name = "%s"%spider.name
        self.client = pymongo.MongoClient("mongodb://mongo:27017")
        self.db = self.client['tripadvisor']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
