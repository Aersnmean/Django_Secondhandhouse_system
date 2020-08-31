# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
import pymongo
from .items import *
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class DB(object):
    def connect(self, col_name):
        client = pymongo.MongoClient(host=settings.get('MONGODB_HOST'), port=settings.get('MONGODB_PORT'))
        self.db = client[settings.get('MONGODB_DB')]
        return self.db[col_name]


class AnjukeSpiderPipeline(DB):
    def __init__(self):
        super().__init__()
        self.col = self.connect('TaiYuanHouse')

    def process_item(self, item, spider):
        if isinstance(item, House):
            self.col.insert(dict(item))
            return item
        return item
