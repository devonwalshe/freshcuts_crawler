# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import datetime
from scrapy.shell import inspect_response
from scrapy.http import Request
from dateutil import parser
from crawler.items import OmniProductItem
import logging

class DonaldrussellAllSpider(scrapy.spiders.CrawlSpider):
    name = 'donaldrussell_all'
    allowed_domains = ['www.donaldrussell.com']
    start_urls = ['http://www.donaldrussell.com/']
    custom_settings = {
            'ITEM_PIPELINES' : { 'crawler.pipelines.OmniProductPipeline': 300,},
            'DOWNLOAD_DELAY' : 1
    }
    rules = (
            Rule(LinkExtractor(allow=(r'/meat/|/poultry-game/|/fish-seafood/'))),
            Rule(LinkExtractor(allow=(r'.*[^-]\w\d+?\.html')),  callback='parse_item', follow=True),
            )

    def parse_item(self, response):
        item = OmniProductItem()
        try:
            item['description'] = response.xpath('.//div[@class="product-desc"]//div[@class="std"]/text()').extract()
        except:
            item['description'] = None
        if response.xpath(r'.//table[contains(@class, "grouped-items-table")]'):
            # scrape each one with yield    
            logging.info("is a list page")
            items = response.xpath(r'.//table[contains(@class, "grouped-items-table")]/tbody//tr')
            for page_item in items:
                try:
                    item['title'] = page_item.xpath('.//div[@class="group-prodname"]/text()').extract()[0]
                except:
                    item['title'] = None
                try:
                    if page_item.xpath('.//span[@class="regular-price"]/span').re(r'[.\d]+'):
                        item['price'] = page_item.xpath('.//span[@class="regular-price"]/span').re(r'[.\d]+')[0]
                    elif page_item.xpath('.//p[contains(@class,"-price")]'):
                        item['price'] = page_item.xpath('.//p[contains(@class,"-price")]//span[@class="price"]/text()').re(r'[.\d]+')[0]
                        item['discount'] = 1 - (float(page_item.xpath('.//p[contains(@class,"-price")]//span[@class="price"]/text()').re(r'[.\d]+')[1]) / float(item['price']))
                except:
                    item['price'] = None
                    item['discount'] = None
                try:
                    ppkg = page_item.xpath('.//div[@class="price-perkg"]//span/text()').re(r'[\.\d]+')[0]
                except:
                    ppkg = None
                try:
                    item['weight'] = float(item['price']) * (1- float(item['discount'])) / float(ppkg)
                except:
                    item['weight'] = None
                try:
                    item['url'] = response.url
                except:
                    item['url'] = None
                try:
                    item['product_id'] = page_item.xpath(r'.//div[@class="group-sku"]/text()').re(r'\w\d+')[0]
                except:
                    item['product_id'] = None
                try:
                    stock = True if response.xpath('.//div[@class="nosto_product"]/span[@class="availability"]/text()').extract()[0] \
                        == "InStock" else False
                except:
                    stock=None
                item['in_stock'] = stock
                try:
                    item['image_url'] = response.xpath('.//div[@class="nosto_product"]/span[@class="image_url"]/text()').extract()[0]
                except:
                    item['image_url'] = None
                item['crawled_at'] = datetime.datetime.now()

                yield(item)

        else:
            logging.info("isn't a list page")
            # do something else 
            
            try:
                item['title'] = response.xpath('.//div[@class="nosto_product"]/span[@class="name"]/text()').extract()[0]
            except:
                item['title'] = None
            try:
                item['price'] = response.xpath('.//div[@class="nosto_product"]/span[@class="price"]/text()').extract()[0]
            except:
                item['price'] = None
            try:
                item['discount'] = None
            except:
                item['discount'] = None
            try:
                ppkg = response.xpath(r'.//div[@class="price-perkg"]')
            except:
                ppkg = None
            try:
                item['weight'] = float(item['price']) / float(response.xpath(r'.//div[@class="price-perkg"]//span[@class="price"]/text()').re(r'[\d\.]+')[0])
            except:
                item['weight'] = None
            try:
                item['url'] = response.xpath('.//div[@class="nosto_product"]/span[@class="url"]/text()').extract()[0]
            except:
                item['url'] = None
            try:
                item['product_id'] = response.xpath(r'.//div[@class="sku"]/text()').re(r'\w\d+')[0]
            except:
                item['product_id'] = None
            try:
                stock = True if response.xpath('.//div[@class="nosto_product"]/span[@class="availability"]/text()').extract()[0] \
                    == "InStock" else False
            except:
                stock=None
            item['in_stock'] = stock
            try:
                item['image_url'] = response.xpath('.//div[@class="nosto_product"]/span[@class="image_url"]/text()').extract()[0]
            except:
                item['image_url'] = None
            item['crawled_at'] = datetime.datetime.now()

            yield(item)


class DonaldrussellSingleSpider(scrapy.Spider):
    name = 'donaldrussell_single'
    allowed_domains = ['www.donaldrussell.com']

    #Set the spider to start on the supplied url from command line
    def __init__(self, *args, **kwargs): 
      super(MySpider, self).__init__(*args, **kwargs) 

      self.start_urls = [kwargs.get('start_url')] 

    def parse(self, response):
        pass
