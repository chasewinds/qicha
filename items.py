# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 15:57:33 2016

@author: Administrator
"""

import scrapy

class DmozItem(scrapy.Item):
    name = scrapy.Field()
    information = scrapy.Field()
    mail = scrapy.Field()
    title = scrapy.Field()
    note = scrapy.Field()
    introduce = scrapy.Field()