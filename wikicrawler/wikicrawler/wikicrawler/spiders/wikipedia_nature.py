# -*- coding: utf-8 -*-
from wikicrawler.common.wikispider import WikiSpider


class WikipediaNatureSpider(WikiSpider):

    name = 'wikipedia_nature'
    start_urls = ['https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D1%80%D0%B8%D1%80%D0%BE%D0%B4%D0%B0']
