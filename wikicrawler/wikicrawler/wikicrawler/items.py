# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikiArticleItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content_file = scrapy.Field()
    categories = scrapy.Field()

