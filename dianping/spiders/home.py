# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy import Spider, Request

from dianping.dz_location import getlocation
from dianping.items import HomeItem


class HomeSpider(scrapy.Spider):
    name = 'home'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/shenzhen/ch90']
    custom_settings = {
        'LOG_FILE': 'log_home.txt',
    }

    def parse(self, response):
        print('parse response.url:' + response.url)
        self.logger.debug('parse response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list_decoration)
        le = LinkExtractor(restrict_css='#J_shopsearch > div:nth-child(2) > div > ul')
        print('1' * 50)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_region)

    def parse_region(self, response):
        print('parse_region response.url:' + response.url)
        self.logger.debug('parse_region response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list_decoration)
        le = LinkExtractor(restrict_css='#J_shopsearch > div:nth-child(2) > div > ul')
        print('2' * 100)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_classfy)

    def parse_classfy(self, response):
        print('parse_classfy response.url:' + response.url)
        self.logger.debug('parse_classfy response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list_decoration)
        le = LinkExtractor(restrict_css='#J_shopsearch > div:nth-child(1) > div > ul')
        print('3' * 150)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            # if link.text.strip() in ['装修设计', '家装卖场']:
            if link.url.split('/')[-1].split('r')[0] in ['g25475', 'g32704']:
                yield Request(link.url, callback=self.parse_list_decoration)
            else:
                yield Request(link.url, callback=self.parse_list)

    def parse_list_decoration(self, response):
        print('parse_list_decoration response.url:' + response.url)
        self.logger.debug('parse_list_decoration response.url:' + response.url)
        item = HomeItem()

        div = response.css('.shop-list>.shop-list-item')
        print('parse_list_decoration li:{}  response.url: {}'.format(div.css('.shop-title>h3>a::text').extract(), response.url))
        self.logger.debug('parse_list_decoration li:{}  response.url: {}'.format(div.css('.shop-title>h3>a::text').extract(), response.url))
        for i in div:
            item['title'] = i.css('.shop-title>h3>a::text').extract_first().strip()
            item['url'] = 'https:' + i.css('.shop-title>h3>a::attr(href)').extract_first()
            if i.css('.shop-images img::attr(data-src)').extract_first():
                item['img'] = 'http:' + i.css('.shop-images img::attr(data-src)').extract_first()
            else:
                item['img'] = 'http:' + i.css('.shop-images img::attr(src)').extract_first()
            # item['star'] = float(
            #     re.search(r'[1-9]\d*|0', i.css('.item-rank-rst::attr(class)').extract_first())[0]) / 10
            item['star'] = float(i.css('.item-rank-rst::attr(class)').re_first(r'[1-9]\d*|0')) / 10
            # item['review_num'] = re.search(r'[1-9]\d*|0', i.css('.shop-info-text-i>a::text').extract_first())[0]
            item['review_num'] = i.css('.shop-info-text-i>a::text').re_first(r'[1-9]\d*|0')
            item['contract_price'] = i.css('div.row.shop-info-text-i > span:nth-child(3)::text').extract_first()
            if len(i.css('.ml-26').extract()) > 1:
                types = i.css('div.row.shop-info-text-i > span:nth-child(4) a::text').extract()
                print("types{} len(types){} len(i.css('.ml-26').extract()) : {}".format(types, len(types),
                                                                                        len(i.css('.ml-26').extract())))
                item['type'] = ' '.join(types)
                print("item['type'] : {}".format(item['type']))
            else:
                item['type'] = '装修设计'
            loc = i.css('.shop-location>span::text').extract()
            if len(loc) == 2:
                item['district'] = loc[0]
                item['location'] = loc[1]
            else:
                item['district'] = loc[0]
                item['location'] = ''
            # item['district'] = i.css('.shop-location>span:first-child::text').extract_first()
            # item['location'] = i.css('.shop-location>span:last-child::text').extract_first()
            if i.css('.shop-team').extract():
                item['design'] = i.css('.shop-team i:first-child::text').extract_first()
                item['designer'] = i.css('.shop-team i:last-child::text').extract_first()
            getlocation(item)
            item['number'] = item['url'].split('/')[-1]
            yield item

        le = LinkExtractor(restrict_css='div.pages a.nextPage')
        print('4' * 200)
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            print('parse_list_decoration next_url:', next_url)
            self.logger.debug('parse_list_decoration next_url:{}'.format(next_url))
            yield Request(next_url, callback=self.parse_list_decoration)

    def parse_list(self, response):
        print('parse_list response.url:' + response.url)
        self.logger.debug('parse_list response.url:' + response.url)
        item = HomeItem()

        li = response.css('.shop-list>.shop-list-item')
        for i in li:
            item['title'] = i.css('.shop-title>h3>a::text').extract_first().strip()
            item['url'] = 'https:' + i.css('.shop-title>h3>a::attr(href)').extract_first()
            if i.css('.shop-images img::attr(data-src)').extract_first():
                item['img'] = 'http:' + i.css('.shop-images img::attr(data-src)').extract_first()
            else:
                item['img'] = 'http:' + i.css('.shop-images img::attr(src)').extract_first()
            item['star'] = float(i.css('.item-rank-rst::attr(class)').re_first(r'[1-9]\d*|0')) / 10
            item['review_num'] = int(i.css('.user-comment>a::text').re_first(r'[1-9]\d*|0'))
            td = i.css('.shop-info-text-i>span::text').extract()
            print('td : {}'.format(td))
            if len(td) == 4:
                item['type'] = ' '.join((td[0], td[1]))
                item['district'] = td[2]
                item['location'] = td[3]
            elif len(td) == 3:
                item['type'] = td[0]
                item['district'] = td[1]
                item['location'] = td[2]
            elif len(td) == 2:
                item['type'] = td[0]
                item['district'] = td[1]
                item['location'] = ''
            else:
                print('td in else: {}'.format(td))
            getlocation(item)
            item['number'] = item['url'].split('/')[-1]
            yield item

        le = LinkExtractor(restrict_css='div.pages a.nextPage')
        print('4' * 200)
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            print('parse_list next_url:', next_url)
            self.logger.debug('parse_list next_url:{}'.format(next_url))
            yield Request(next_url, callback=self.parse_list)
