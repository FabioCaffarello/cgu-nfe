import os

import pymongo
import scrapy
import yaml
from dotenv import load_dotenv
from itemadapter import ItemAdapter

from . import metadata, settings


dotenv_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "../..", ".env"))

load_dotenv(dotenv_path)


class MongoClient:
    def __init__(self):
        self.host = "mongodb://mongodb:27017/"
        self.username = os.getenv("MONGODB_USERNAME")
        self.password = os.getenv("MONGODB_PASSWORD")

    def _mongo_client(self):
        connection = pymongo.MongoClient(
            self.host,
            username=self.username,
            password=self.password
        )
        return connection

    def _setup_collection(self, database, collection):
        mongo_client = self._mongo_client()
        db = mongo_client[database]
        mongo_collection = db[collection]
        return mongo_collection


class CguNfeMetadataPipeline(MongoClient):
    def __init__(self):
        super().__init__()
        self._dir_schem = "schemas/output-schema.yaml"
        self._path_schema = os.path.realpath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                self._dir_schem
            )
        )

    def open_spider(self, spider):
        mongo = self._setup_collection(database="metadata", collection="cgu_nfe")
        with open(self._path_schema, "r") as schema:
            _metadata = yaml.safe_load(schema)

        _processing_metadata = metadata.GenerateProcessingMetadata(bot_name="cgu_nfe")
        processing_metadata = _processing_metadata.processing_data

        _metadata["metadata"]["_metadata"].update(**processing_metadata)
        mongo.replace_one({
            "_metadata.processingId": _metadata["metadata"]["_metadata"]["processingId"]
            },
            dict(_metadata["metadata"]),
            upsert=True
        )
        spider.log("Metadata Saved!")
        pass


class CguNfePipeline(MongoClient):
    def __init__(self):
        super().__init__()
        self.chaveDeAcesso = set()

    def process_item(self, item, spider):
        _processing_metadata = metadata.GenerateProcessingMetadata(bot_name="cgu_nfe")
        processing_metadata = _processing_metadata.processing_data
        mongo = self._setup_collection(database="output", collection="cgu_nfe")
        if item["chaveDeAcesso"] not in self.chaveDeAcesso:
            item["metadata"] = processing_metadata
            # item.add_value('metadata', processing_metadata)
            self.chaveDeAcesso.add(item["chaveDeAcesso"])
            mongo.replace_one({
                "chaveDeAcesso": item["chaveDeAcesso"],
                "metadata.processingId": item["metadata"]["processingId"],
                },
                dict(item),
                upsert=True
            )
            spider.log("Record Saved!")
            return item
        else:
            raise scrapy.exceptions.DropItem(f"Duplicate item found: {item}")
