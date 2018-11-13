# -*- coding: utf-8 -*-
import json
import re

import scrapy
from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor

from dianping.dz_location import getlocation
from dianping.items import FilmItem, FilmItem2


class Film2Spider(Spider):
    name = 'film2'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/shenzhen/ch25']
    custom_settings = {
        'LOG_FILE': 'log_film2.txt',
    }
    def parse(self, response):
        le = LinkExtractor(restrict_css='#region-nav')
        print('11111111111111111111111111111111')
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_region)

    def parse_region(self, response):
        le = LinkExtractor(restrict_css='#region-nav-sub')
        print('22222222222222222222222222222222222')
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_classfy)

    def parse_classfy(self, response):
        le = LinkExtractor(restrict_css='#classfy')
        print('33333333333333333333333333333333333333')
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_list)

    def parse_list(self, response):
        item = FilmItem2()

        li = response.css('#shop-all-list>ul>li')
        print('parse_list li:{}  response.url: {}'.format(li.css('.txt>.tit h4::text').extract(), response.url))
        self.logger.debug('parse_list li:{}  response.url: {}'.format(li.css('.txt>.tit h4::text').extract(), response.url))
        for i in li:
            item['title'] = i.css('.txt>.tit h4::text').extract_first().strip()
            item['url'] = i.css('.txt>.tit>a::attr(href)').extract_first()
            if i.css('.shop-branch::text'):
                item['branch'] = i.css('.shop-branch::attr(href)').extract_first()
            item['img'] = i.css('img::attr(data-src)').extract_first()
            item['star'] = float(i.css('.sml-rank-stars::attr(class)').re_first(r'[1-9]\d*|0')) / 10
            if i.css('.review-num b::text'):
                print('review-num : {}'.format(i.css('.review-num>b::text').extract_first()))
                item['review_num'] = int(i.css('.review-num>b::text').extract_first())
            if i.css('.mean-price b::text'):
                item['mean_price'] = i.css('.mean-price b::text').extract_first().strip('￥')
            print('type location 1: {}'.format(i.css('.tag-addr span::text').extract()))
            item['type'] = i.css('.tag-addr span::text').extract()[0].strip()
            item['location'] = i.css('.tag-addr span::text').extract()[1].strip()
            # item['address'] = i.css('.addr::text').extract_first().strip()
            # getlocation(item)
            item['number'] = item['url'].split('/')[-1]
            request = Request(item['url'], callback=self.parse_list_detail)
            request.meta['item'] = item  # 将item暂存
            yield request

        le = LinkExtractor(restrict_css='div.page > a.next')
        print('4' * 50)
        links = le.extract_links(response)
        # print(links, links.url, links.text)
        if links:
            next_url = links[0].url
            print('next_url:', next_url)
            yield Request(next_url, callback=self.parse_list)

    def parse_list_detail(self, response):
        item = response.meta['item']
        print('item:', item)
        print('response.text:', response, response.text, response.url)
        m = re.findall('window.shop_config=(.*), shopEvtId:', response.text)
        print('m:{}', m)
        result = m[0] + '}'
        print('result: {}'.format(result))
        item['address'] = result.get('address')
        item['lat'] = result.get('shopGlat')
        item['lng'] = result.get('shopGlng')
        yield item
