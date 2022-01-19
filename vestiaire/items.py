# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VestiaireItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    # output = scrapy.Field()
    category = scrapy.Field()
    gender = scrapy.Field()
    itemId = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    subCategory = scrapy.Field()
    price = scrapy.Field()
    finalPrice = scrapy.Field()
    estimatedRetailPrice = scrapy.Field()
    currency = scrapy.Field()
    qualityCost = scrapy.Field()
    fetchDate = scrapy.Field()
    model = scrapy.Field()
    color = scrapy.Field()
    material = scrapy.Field()
    style = scrapy.Field()
    condition = scrapy.Field()
    onlineSince = scrapy.Field()
    inclusions = scrapy.Field()
    height = scrapy.Field()
    width = scrapy.Field()
    depth = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    images = scrapy.Field()
