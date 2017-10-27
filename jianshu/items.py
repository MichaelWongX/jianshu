# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity, Join,MapCompose,Compose

class JianshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Author(scrapy.Item):
    author_id = Field()
    author_name = Field()
    following_num = Field()
    following_list = Field()
    fans_num = Field()
    fans_list = Field()
    article_num = Field()
    article_list = Field()
    char_num = Field()
    likes = Field()
    description = Field()




class Article(scrapy.Item):

    author_id = Field()
    author_name = Field()
    title = Field()
    content = Field(output_processor=Join())
    pub_time = Field()
    note = Field()
    article_url = Field()


class JianshuItemLoader(ItemLoader):
    default_output_processor = TakeFirst()



