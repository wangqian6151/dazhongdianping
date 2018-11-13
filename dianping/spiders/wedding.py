# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy import Spider, Request

from dianping.dz_location import getlocation
from dianping.items import WeddingItem


class WeddingSpider(scrapy.Spider):
    name = 'wedding'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/shenzhen/ch55']
    custom_settings = {
        'LOG_FILE': 'log_wedding.txt',
    }

    def parse(self, response):
        print('parse response.url:' + response.url)
        self.logger.debug('parse response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='.t-district.J_li > div > div.t-list > ul')
        print('1' * 50)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_region)

    def parse_region(self, response):
        print('parse_region response.url:' + response.url)
        self.logger.debug('parse_region response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='.t-district.J_li > div > div.t-list.tsub-list > ul')
        print('2' * 100)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_classfy)

    def parse_classfy(self, response):
        print('parse_classfy response.url:' + response.url)
        self.logger.debug('parse_classfy response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='.t-type.J_li > div > div.t-list > ul')
        print('3' * 150)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            if link.url.split('/')[-1].split('r')[0] in ['g165']:
                print('parse_classfy 婚宴 response.url:' + response.url)
                self.logger.debug('parse_classfy 婚宴 response.url:' + response.url)
                # yield Request(link.url, callback=self.parse_list)
            else:
                yield Request(link.url, callback=self.parse_list)

    def parse_list(self, response):
        print('parse_list response.url:' + response.url)
        self.logger.debug('parse_list response.url:' + response.url)
        item = WeddingItem()

        li = response.css('.shop-list>li')
        print('parse_list li:{}  response.url: {}'.format(li.css('.shopname::text').extract(), response.url))
        self.logger.debug('parse_list li:{}  response.url: {}'.format(li.css('.shopname::text').extract(), response.url))
        for i in li:
            item['title'] = i.css('.shopname::text').extract_first()
            item['url'] = 'http:' + i.css('.shopname::attr(href)').extract_first().split('?')[0]
            if i.css('a img::attr(data-lazyload)').extract_first():
                item['img'] = 'http:' + i.css('a img::attr(data-lazyload)').extract_first()
            else:
                item['img'] = 'http:' + i.css('a img::attr(src)').extract_first()
            item['star'] = float(i.css('.item-rank-rst::attr(class)').re_first(r'[1-9]\d*|0')) / 10
            if i.css('p.remark > span:nth-child(2) > a::text').re_first(r'[1-9]\d*|0'):
                item['review_num'] = int(i.css('p.remark > span:nth-child(2) > a::text').re_first(r'[1-9]\d*|0'))
            if i.css('.price::text').extract_first().strip() != '-':
                item['mean_price'] = int(i.css('.price::text').extract_first().strip().strip('￥'))
            item['product_photos'] = i.css('p.remark > span:nth-child(3) > a::text').extract_first()
            if i.css('.area-list::text').extract_first():
                item['location'] = ' '.join(i.css('.area-list::text').extract_first().strip().split())
            else:
                item['location'] = ''
            getlocation(item)
            item['number'] = item['url'].split('/')[-1]
            yield item

        le = LinkExtractor(restrict_css='div.Pages > a.NextPage')
        print('4' * 200)
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            print('parse_list next_url:', next_url)
            self.logger.debug('parse_list next_url:{}'.format(next_url))
            yield Request(next_url, callback=self.parse_list)
