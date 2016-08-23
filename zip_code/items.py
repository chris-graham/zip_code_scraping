# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZipCodeItem(scrapy.Item):
    city = scrapy.Field()
    zip_code = scrapy.Field()
    zip_percent = scrapy.Field()

class CountyItem(scrapy.Item):
	county = scrapy.Field()
	fips = scrapy.Field()
	ZipCodeItem = ZipCodeItem()

class StateItem(scrapy.Item):
	state = scrapy.Field()
	CountyItem = CountyItem()