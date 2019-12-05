# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HuodongjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    meeting=scrapy.Field()#会议名字段
    date=scrapy.Field()#日期字段
    place=scrapy.Field()#地点字段
    industry=scrapy.Field()#行业字段
    pass

