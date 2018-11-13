# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy import Spider, Request

from dianping.dz_location import getlocation
from dianping.items import BabyItem


class BabySpider(Spider):
    name = 'baby'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/shenzhen/ch70']

    custom_settings = {
        'LOG_FILE': 'log_baby.txt',
    }

    def parse(self, response):
        print('parse response.url:' + response.url)
        self.logger.debug('parse response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='.t-district')
        print('1' * 50)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_region)

    def parse_region(self, response):
        print('parse_region response.url:' + response.url)
        self.logger.debug('parse_region response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='.tsub-list')
        print('2' * 100)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_classfy)

    def parse_classfy(self, response):
        print('parse_classfy response.url:' + response.url)
        self.logger.debug('parse_classfy response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='.t-type')
        print('3' * 150)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_list)

    def parse_list(self, response):
        print('parse_list response.url:' + response.url)
        self.logger.debug('parse_list response.url:' + response.url)
        item = BabyItem()

        li = response.css('.shop-list>li')
        print('parse_list li:{}  response.url: {}'.format(li.css('.shopname::text').extract(), response.url))
        self.logger.debug('parse_list li:{}  response.url: {}'.format(li.css('.shopname::text').extract(), response.url))
        for i in li:
            item['title'] = i.css('.shopname::text').extract_first()
            item['url'] = 'http:' + i.css('.shopname::attr(href)').extract_first()
            if i.css('a img::attr(data-lazyload)').extract_first():
                item['img'] = 'http:' + i.css('a img::attr(data-lazyload)').extract_first()
            else:
                item['img'] = 'http:' + i.css('a img::attr(src)').extract_first()
            item['star'] = float(i.css('.item-rank-rst::attr(class)').re_first(r'[1-9]\d*|0')) / 10
            if i.css('.comment-count a::text').re_first(r'[1-9]\d*|0'):
                item['review_num'] = int(i.css('.comment-count a::text').re_first(r'[1-9]\d*|0'))
            item['mean_price'] = i.css('.price::text').extract_first()
            if i.css('.product-count a::text').extract_first():
                item['product_photos'] = i.css('.product-count a::text').extract_first().strip('"')
            if i.css('.key-list::text').extract_first():
                item['location'] = ' '.join(i.css('.key-list::text').extract_first().strip().split())
            else:
                item['location'] = ''
            getlocation(item)
            item['number'] = item['url'].split('/')[-1]
            yield item

        le = LinkExtractor(restrict_css='div.Pages > a.NextPage')
        print('4' * 200)
        links = le.extract_links(response)
        # print(links, links.url, links.text)
        if links:
            next_url = links[0].url
            print('next_url:', next_url)
            yield Request(next_url, callback=self.parse_list)
