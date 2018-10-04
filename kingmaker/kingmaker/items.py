# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Comment(scrapy.Item):
    author = scrapy.Field()
    timestamp = scrapy.Field()
    text = scrapy.Field()
    is_deleted = scrapy.Field()
