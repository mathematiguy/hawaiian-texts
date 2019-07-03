# -*- coding: utf-8 -*-
import scrapy
import logging
from bs4 import BeautifulSoup

def clean_text(texts):
    '''
    Clean the body text for a given xpath tag
    '''
    clean_texts = []
    for text in texts:
        soup = BeautifulSoup(text, 'lxml')
        for p in soup.findAll('p'):
            clean_texts.append(p.text.replace("\n", " "))
    return '\n'.join(clean_texts)

def clean_columns(columns):
    clean_cols = []
    for col in columns:
        soup = BeautifulSoup(col, 'lxml')
        for td in soup.findAll('td'):
            clean_cols.append(td.text.replace("\n", " "))
    return '\n'.join(clean_cols)

def clean_title(titles):
    title_texts = []
    for title in titles:
        soup = BeautifulSoup(title, 'lxml')
        for h3 in soup.findAll("h3"):
            title_texts.append(h3.text)
    return '\n'.join(title_texts)

class NupepaSpider(scrapy.Spider):
    name = 'nupepa'
    allowed_domains = ['nupepa.org']
    start_urls = ['http://nupepa.org/gsdl2.5/cgi-bin/nupepa?e=d-0nupepa--00-0-0--010---4-----text---0-1l--1haw-Zz-1---20-about---0003-1-0000utfZz-8-00&a=d&cl=CL1']

    def parse(self, response):
        newspaper_tags = response.xpath("//table/tr[@valign='top']/td[@valign='center']/a/@href")
        for tag in newspaper_tags:
            newspaper_url = response.urljoin(tag.extract())
            if newspaper_url.endswith("=text"):
                yield scrapy.Request(newspaper_url, callback = self.parse_text)
            yield scrapy.Request(newspaper_url, callback = self.parse)

    def parse_text(self, response):
        text_tags = response.xpath('//div[contains(@class,"Section1")]/p')
        title = response.xpath('//h3').extract()
        text_list = clean_text(text_tags.extract())
        column_tags = response.xpath("//tr/td")
        column_texts = clean_columns([m.encode('utf-8') for m in column_tags.extract()])
        text_list += column_texts
        yield {'text': text_list, 'title': clean_title(title), 'url': response.url}
        next_page = response.xpath("/html/body/center[7]/table/tbody/tr/td[2]/a[1]/@href")
        next_page = response.urljoin(next_page)
        yield scrapy.Request(next_page, callback = self.parse_text)
