# -*- coding: utf-8 -*-
from wikicrawler.common.wikispider import WikiSpider


class WikipediaHumanSpider(WikiSpider):

    name = 'wikipedia_human'
    start_urls = ['https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A7%D0%B5%D0%BB%D0%BE%D0%B2%D0%B5%D0%BA']
