# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy_mongodb import MongoDBPipeline
import datetime
import logging

class JianshuPipeline(object):
    def process_item(self, item, spider):
        return item

class MyMongoDBPipeline(MongoDBPipeline):

    def __init__(self, **kwargs):
        """ Constructor """
        super(MyMongoDBPipeline, self).__init__(**kwargs)
        self.logger = logging.getLogger('scrapy-mongodb-pipeline')

    def process_item(self, item, spider):
        """ Process the item and add it to MongoDB,
        the item can be Item object or dict

        :type item: Item object, or dict
        :param item: The item to put into MongoDB
        :type spider: BaseSpider object
        :param spider: The spider running the queries
        :returns: Item object
        """
        item = dict(self._get_serialized_fields(item))

        item = dict((k, v) for k, v in item.items() if v is not None and v != "")

        if self.config['buffer']:
            self.current_item += 1

            if self.config['append_timestamp']:
                item['scrapy-mongodb'] = {'ts': datetime.datetime.utcnow()}

            self.item_buffer.append(item)

            if self.current_item == self.config['buffer']:
                self.current_item = 0

                try:
                    return self.insert_item(self.item_buffer, spider)
                finally:
                    self.item_buffer = []

            return item

        return self.insert_item(item, spider)