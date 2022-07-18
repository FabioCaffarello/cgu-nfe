# import os

# import scrapy
# from itemadapter import ItemAdapter


# class DeleteOutputPipeline:
#     def open_spider(self, spider):
#         try:
#             os.remove("../data/output.jsonl")
#         except OSError as e:
#             pass


# class CguNfePipeline:
#     def __init__(self):
#         self.chaveDeAcesso = set()

#     def process_item(self, item, spider):
#         if item['chaveDeAcesso'] in self.chaveDeAcesso:
#             raise scrapy.exceptions.DropItem(f"Duplicate item found: {item}")
#         else:
#             self.chaveDeAcesso.add(item['chaveDeAcesso'])
#             return item

import os

import pymongo
import scrapy
from itemadapter import ItemAdapter
import urllib.parse
from . import settings

# class DeleteOutputPipeline:
#     def open_spider(self, spider):
#         try:
#             os.remove("../data/output.jsonl")
#         except OSError as e:
#             pass


class CguNfePipeline:
    def __init__(self):
        self.chaveDeAcesso = set()
        host = "mongodb://localhost:27017/"
        self.connection = pymongo.MongoClient(
            host
        )
        self.db = self.connection["portalTransparencia"]
        self.collection = self.db["Nfe"]

    def process_item(self, item, spider):
        if item['chaveDeAcesso'] not in self.chaveDeAcesso:
            self.chaveDeAcesso.add(item['chaveDeAcesso'])
            self.collection.replace_one({"chaveDeAcesso": item['chaveDeAcesso']}, dict(item), upsert=True)
            spider.log("Record Saved!")
            return item
        else:
            raise scrapy.exceptions.DropItem(f"Duplicate item found: {item}")

