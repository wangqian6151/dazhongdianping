# -*- coding: utf-8 -*-
import json
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy import Spider, Request

from dianping.dz_location import getlocation
from dianping.items import HotelItem


class HotelSpider(scrapy.Spider):
    name = 'hotel'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/shenzhen/hotel/']
    custom_settings = {
        'LOG_FILE': 'log_hotel.txt',
    }

    def parse(self, response):
        print('parse response.url:' + response.url)
        self.logger.debug('parse response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='.sub-filter-wrapper')
        print('1' * 50)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_list_first)

    def parse_list_first(self, response):
        maxpage = 0
        if response.css('.page .next'):
            # maxpage = int(e('.PageLink:last').attr('data-ga-page'))
            maxpage = int(response.css('.page a::text').extract()[-2])
        elif len(response.css('.page a').extract()) == 1:
            maxpage = 1
        else:
            print('maxpage in else: {}'.format(maxpage))
        print('maxpage: {}'.format(maxpage))
        self.logger.debug('maxpage: ' + str(maxpage))
        print('response.url ' + response.url)
        self.logger.debug('response.url ' + response.url)
        baseurl = str(response.url)
        for i in range(maxpage, 0, -1):
            url = baseurl + 'p' + str(i)
            yield Request(url, callback=self.parse_list)

    def parse_list(self, response):
        print('parse_list response.url:' + response.url)
        self.logger.debug('parse_list response.url:' + response.url)
        item = HotelItem()

        m = re.findall('{"hotelList":(.*),"sortInfo"', response.text)
        print('parse_list m: {}'.format(m))
        self.logger.debug('parse_list m: {}'.format(m))

        result = json.loads(m[0] + '}')

        for record in result.get('records'):
            item['title'] = record.get('shopName')
            item['url'] = 'http://www.dianping.com' + record.get('shopUrl')
            item['is_bookable'] = record.get('isBookable')
            item['location'] = record.get('regionName')
            item['walk_distance'] = record.get('distanceText')
            item['price'] = record.get('price')
            item['star'] = record.get('star') / 10
            item['review_num'] = record.get('reviewCount')
            item['number'] = record.get('id')
            item['pic_array'] = str(record.get('picArray')).replace('\'', '').strip('[').strip(']')
            getlocation(item)
            yield item

        le = LinkExtractor(restrict_css='.page .next')
        print('4' * 200)
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            print('parse_list next_url:', next_url)
            self.logger.debug('parse_list next_url:{}'.format(next_url))
            yield Request(next_url, callback=self.parse_list)
