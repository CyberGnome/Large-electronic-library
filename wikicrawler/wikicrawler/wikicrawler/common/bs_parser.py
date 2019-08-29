# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


class BS4Parser:
    excluded_blocks = []
    added_tags = []

    def bs4parse_text(self, text):
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

    @staticmethod
    def delete_blank_paragraphs(content):
        soup = BeautifulSoup(content, 'html.parser')

        titles = ['h1', 'h2', 'h3',
                  'h4', 'h5', 'h6']

        prev = None

        for line in soup:
            if prev:
                if prev.name in titles and prev.name == line.name:
                    prev.extract()
            prev = line

        if prev.name in titles:
            prev.extract()

        return soup.prettify()

    @staticmethod
    def file_is_fit(content):
        titles = ['h1', 'h2', 'h3',
                  'h4', 'h5', 'h6']

        text = 'p'
        title_c, text_c = 0, 0

        soup = BeautifulSoup(content, 'html.parser')
        for line in soup:
            if line.name in titles:
                title_c += 1
            elif line.name == text:
                text_c += 1

        if title_c - 1 > text_c:
            return False
        else:
            return True
