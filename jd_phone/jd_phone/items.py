# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdPhoneItem(scrapy.Item):
    name = scrapy.Field()
    params = scrapy.Field()
    price = scrapy.Field()
    question = scrapy.Field()
    price_id = scrapy.Field()
    store = scrapy.Field()
    city = scrapy.Field()
    sale = scrapy.Field()
    url = scrapy.Field()