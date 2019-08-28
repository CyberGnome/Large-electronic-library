# -*- coding: utf-8 -*-
from wikicrawler.common.wikispider import WikiSpider


class WikipediaTechniqueSpider(WikiSpider):

    name = 'wikipedia_technique'
    start_urls = ['https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A2%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0']
