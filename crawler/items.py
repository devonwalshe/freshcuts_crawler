# -*- coding: utf-8 -*-
import scrapy


class OmniProductItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    discount = scrapy.Field()
    weight = scrapy.Field()
    url = scrapy.Field()
    product_id = scrapy.Field()
    crawled_at = scrapy.Field()
    in_stock = scrapy.Field()
    image_url = scrapy.Field()
    pass
