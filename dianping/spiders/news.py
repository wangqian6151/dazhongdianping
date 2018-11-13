# -*- coding: utf-8 -*-
import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['www.xinhuanet.com']
    start_urls = ['http://www.xinhuanet.com/money/index.htm']

    def parse(self, response):
        li = response.css('#hideData1 li.clearfix')
        for i in li:
            title = i.css('h3>a::text')
            print(title)
            yield {'title': title}
