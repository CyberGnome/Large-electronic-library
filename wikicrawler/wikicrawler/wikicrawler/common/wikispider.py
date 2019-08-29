# -*- coding: utf-8 -*-
import hashlib
import os
from urllib.parse import urljoin

import scrapy
from scrapy import Request

from wikicrawler.items import WikiArticleItem
from wikicrawler.settings import BODY_FILES_STORAGE
from wikicrawler.common.bs_parser import BS4Parser
from wikicrawler.common.exceptions import CrawlException


class WikiSpider(scrapy.Spider, BS4Parser):
    storage = BODY_FILES_STORAGE
    name = 'wiki'
    allowed_domains = ['wikipedia.org']
    start_urls = []

    items_pages = set()
    subcategories_pages = set()

    excluded_blocks = [
        'См. также',
        'Примечания',
        'Литература',
        'Ссылки',
        'Источники'
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

            subcategories_hrefs = response.xpath(subcategories_page_path).extract()
            for subcategory_href in subcategories_hrefs:
                yield response.follow(subcategory_href, callback=self.parse)

    def parse_item(self, response):
        self.items_pages.add(response.request.url)

        item_url = response.request.url

        item_categories = dict()
        try:
            item_title, item_bodyfile, item_categories = self.parse_context(response)
        except CrawlException as exception:
            if exception.errors == exception.FILE_ALREADY_EXISTS:
                item_categories = exception.saved_data
        else:
            article_item = WikiArticleItem()

            article_item['url'] = item_url
            article_item['title'] = item_title
            article_item['content_file'] = item_bodyfile
            article_item['categories'] = item_categories.keys()

            yield article_item
        finally:
            for category in item_categories.keys():
                yield response.follow(item_categories.get(category), callback=self.parse)

    def parse_context(self, response):
        title_path = '//*[@id="firstHeading"]//text()'
        body_path = '/html/body/div[3]/div[3]/div[4]/div'
        categories_path = '//*[@id="mw-normal-catlinks"]//*/a'

        title = response.xpath(title_path).extract_first()
        body = response.xpath(body_path).extract_first()
        body_file = os.path.join(self.storage,
                                 "%s.html" % hashlib.md5(response.request.url.encode('utf-8')).hexdigest())
        categories_block = response.xpath(categories_path)
        categories = {}
        for category in categories_block:
            categories.update({category.xpath('text()').extract_first(): category.xpath('@href').extract_first()})

        if os.path.exists(body_file):
            raise CrawlException("File \"%s\" already exists!" % body_file,
                                 CrawlException.FILE_ALREADY_EXISTS,
                                 categories)

        body = self.bs4parse_text(body)

        f = open(body_file, "w")
        f.write(body)
        f.close()

        return title, body_file, categories
