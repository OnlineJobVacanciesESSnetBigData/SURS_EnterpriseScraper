# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class JobItem(Item):
    url = Field()
    # keyword_url = Field()
    # keyword_url_tab = Field()
    # keyword_tab = Field()

    # Order items for output won't work as suggested here
    # http://stackoverflow.com/questions/20601976/how-to-order-xml-with-item-fields-in-scrapy

    # def keys(self):
    # return ['url', 'keyword_url', 'keyword_url_tab', 'keyword_tab']

