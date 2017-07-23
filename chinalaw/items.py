# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ChinalawItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    gid = scrapy.Field()
    urls = scrapy.Field()
    title2 = scrapy.Field()
    text = scrapy.Field()
    html = scrapy.Field()
    maketime = scrapy.Field()
    subsite = scrapy.Field()
    channel = scrapy.Field()
    category = scrapy.Field()
    author = scrapy.Field()
    pubDate = scrapy.Field()
    source = scrapy.Field()
    location = scrapy.Field()
    department = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    guid = scrapy.Field()
    effectiveTime = scrapy.Field()
    keyword = scrapy.Field()
    rksj = scrapy.Field()

    
class ChinalawBrefItem(scrapy.Item):
    title = scrapy.Field()
    gid = scrapy.Field()
    urls = scrapy.Field()
    uid = scrapy.Field()
    date = scrapy.Field()
    rksj = scrapy.Field()
    