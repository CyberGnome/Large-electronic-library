# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

from wikicrawler.common.bs_parser import BS4Parser
from wikicrawler.settings import HTML_FILES_STORAGE
from wikicrawler.common.exceptions import CrawlException


class DuplicatesPipeline(object):
    def process_item(self, item, spider):
        return item


class EditRawFilePipeline(object):
    @staticmethod
    def __clean_content(content):
        bs4p = BS4Parser()

        content = bs4p.delete_blank_paragraphs(content)

        if bs4p.file_is_fit(content):
            return content
        else:
            return None

    def process_item(self, item, spider):
        title = item['title']
        content_file = item['content_file']

        with open(content_file) as c_file:
            content = c_file.read()

        content = self.__clean_content(("<h1>%s</h1>\n" % title) + content)
        if content is None:
            os.remove(content_file)
            raise CrawlException("File does not fit", CrawlException.FILE_DOESNT_FIT)

        new_file = os.path.join(HTML_FILES_STORAGE, os.path.split(content_file)[1])
        with open(new_file, 'w') as new_file:
            new_file.write(content)

        os.remove(content_file)

        item['content_file'] = new_file
        return item


class CreateCategoriesPipeline(object):
    def process_item(self, item, spider):
        return item


class Save2DatabasePipeline(object):
    def process_item(self, item, spider):
        return item
