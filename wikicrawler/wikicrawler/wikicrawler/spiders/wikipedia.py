# -*- coding: utf-8 -*-
import hashlib
import os
from urllib.parse import urljoin

import scrapy
from scrapy import Request
from bs4 import BeautifulSoup

FILES_STORAGE = 'tmp'


class WikipediaSpider(scrapy.Spider):
    name = 'wikipedia'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D1%80%D0%B8%D1%80%D0%BE%D0%B4%D0%B0',  # Природа
                  #'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A2%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0',  # Техника # Todo
                  #'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A7%D0%B5%D0%BB%D0%BE%D0%B2%D0%B5%D0%BA'   # Человек # Todo
                  ]

    items_pages = set()
    subcategories_pages = set()

    excluded_blocks = [
        'См. также',
        'Примечания',
        'Литература',
        'Ссылки'
    ]

    added_tags = [
        'p', 'h1', 'h2',
        'h3', 'h4', 'h5',
        'h6'
    ]

    def parse(self, response):
        if response.url not in self.subcategories_pages:
            self.subcategories_pages.add(response.url)

            subcategories_page_path = '//*[@id="mw-subcategories"]//*/a/@href'
            item_page_path = '//*[@id="mw-pages"]//*/a/@href'

            items_hrefs = response.xpath(item_page_path).extract()
            for item_href in items_hrefs:
                url = urljoin(response.url, item_href)
                if url not in self.items_pages:
                    yield Request(url, callback=self.parse_item)

            #subcategories_hrefs = response.xpath(subcategories_page_path).extract()
            #for subcategory_href in subcategories_hrefs:
            #    yield response.follow(subcategory_href, callback=self.parse)

    def parse_item(self, response):
        self.items_pages.add(response.request.url)
        item_url = response.request.url
        item_title, item_bodyfile, categories = self.parse_context(response)

        categories_names = categories.keys()

        for category in categories_names:
            yield response.follow(categories.get(category), callback=self.parse)

    def parse_context(self, response):
        title_path = '//*[@id="firstHeading"]//text()'
        body_path = '/html/body/div[3]/div[3]/div[4]/div'
        categories_path = '//*[@id="mw-normal-catlinks"]//*/a'

        title = response.xpath(title_path).extract_first()
        body = response.xpath(body_path).extract_first()
        body_file = os.path.join(FILES_STORAGE,
                                 "%s.html" % hashlib.md5(response.request.url.encode('utf-8')).hexdigest())

        body = self.parse_text(body)

        categories_block = response.xpath(categories_path)
        categories = {}
        for category in categories_block:
            categories.update({category.xpath('text()').extract_first(): category.xpath('@href').extract_first()})

        f = open(body_file, "w")
        f.write(body)
        f.close()

        return title, body_file, categories

    def parse_text(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        body = soup.find("div", {"class": "mw-parser-output"})

        result = []

        for item in body:
            if item.name in self.added_tags:
                checked_item = self.filter_text(item)
                if checked_item:
                    result.append(str(checked_item))
                continue
            if item.name == 'div':
                if item.attrs.get('id') == 'toc':
                    checked_item = self.filter_toc(item)
                    if checked_item:
                        result.append(str(checked_item))

        return BeautifulSoup("\n".join(result), 'html.parser').prettify()

    def filter_text(self, tag):
        edit_sections = tag.findAll('span', {'class': 'mw-editsection'})
        if edit_sections:
            for edit_section in edit_sections:
                edit_section.extract()

        if tag.text in self.excluded_blocks:
            return None

        sups = tag.findAll('sup', {'class': 'reference'})

        for sup in sups:
            sup.extract()

        a_hrefs = tag.findAll('a')
        for a in a_hrefs:
            a.replace_with(a.text)

        return tag

    def filter_toc(self, tag):
        toc = tag
        els = toc.findAll('li')

        for el in els:
            title = el.find('span', {'class': 'toctext'})
            title = self.filter_text(title)
            if not title:
                el.extract()

        return toc
