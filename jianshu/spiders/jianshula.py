# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import Article,Author,JianshuItemLoader
from scrapy.loader import ItemLoader
from scrapy import Request
import re


class JianshulaSpider(CrawlSpider):
    name = 'jianshula'
    allowed_domains = ['jianshu.com']
    start_urls = ['http://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/p/'), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow=r'/users/[0-9a-z]*/following'), callback='parse_following', follow=True),
        Rule(LinkExtractor(allow=r'/users/[0-9a-z]*/followers'), callback='parse_fans', follow=True),
        Rule(LinkExtractor(allow=r'/u/[0-9a-z]*'), callback='parse_author', follow=True),
    )

    def parse_article(self, response):
        loader = JianshuItemLoader(item=Article(),response=response)
        loader.add_xpath('author_id', '//span[@class="name"]/a/@href')
        loader.add_xpath('author_name', '//span[@class="name"]/a/text()')
        loader.add_xpath('title', '//h1[@class="title"]/text()')
        loader.add_xpath('content', '//div[@class="show-content"]//p/text()')
        meta = loader.nested_xpath('//div[@class="meta"]')
        meta.add_xpath('pub_time', './span[@class="publish-time"]/text()')
        meta.add_xpath('content_len', './span[@class="wordage"]/text()')
        meta.add_xpath('readed', './span[@class="view-count"]/text()')
        meta.add_xpath('comments_count','./span[@class="comments-count"]/text')
        meta.add_xpath('likes_count', './span[@class="likes-count"]/text')
        loader.add_value('article_url', response.url)
        return loader.load_item()

    def parse_author(self,response):
        """parse author information"""
        loader = JianshuItemLoader(item=Author(),response=response)
        info = loader.nested_xpath('//div[@class="info"]')
        info.add_xpath('following_num','.//li[1]//p/text()')
        info.add_xpath('fans_num','.//li[2]//p/text()')
        info.add_xpath('article_num','.//li[3]//p/text()')
        info.add_xpath('char_num','.//li[4]//p/text()')
        info.add_xpath('likes', './/li[4]//p/text()')
        loader.add_xpath('description','div[@class="js-intro"]/text()')
        return loader.load_item()

    def parse_following(self,response):
        if re.search('/following/?$',response.url):
            tmp = response.xpath('//div[@class="info"]//li[1]//p/text()').extract_first()
            if tmp.isdigit():
                tmp = int(tmp)
                for i in range(2,tmp//9 +2):
                    url = response.urljoin('?page=%d' % i)
                    yield Request(url=url,callback=self.parse_following)
            else:
                self.logger.log(20, 'can not find the following num %s' % response.url)

        item = Author()
        item['author_id'] = response.xpath('//div[@class="title"]/a/@href').extract_first()
        item['following_list'] = response.xpath('//ul[@class="user-list"]//div[@class="info"]/a/@href').extract()
        yield item
        if item['following_list']:
            for url in item['following_list']:
                yield Request(url=response.urljoin(url))


    def parse_fans(self,response):
        if re.search('/followers/?$',response.url):
            tmp = response.xpath('//div[@class="info"]//li[2]//p/text()').extract_first()
            if tmp.isdigit():
                tmp = int(tmp)
                max = 101 if tmp > 900 else (tmp//9 + 2)
                for i in range(2,max):
                    url = response.urljoin('?page=%d' % i)
                    yield Request(url=url,callback=self.parse_fans)
            else:
                self.logger.log('INFO', 'can not find the following num %s' % response.url)

        item = Author()
        item['author_id'] = response.xpath('//div[@class="title"]/a/@href').extract_first()
        item['fans_list'] = response.xpath('//ul[@class="user-list"]//div[@class="info"]/a/@href').extract()
        yield item
        if item['fans_list']:
            for url in item['fans_list']:
                yield Request(url=response.urljoin(url))

