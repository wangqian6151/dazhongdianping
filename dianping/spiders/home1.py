# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider

from dianping.dz_location import dz_location, getlocation
from dianping.items import HomeItem


class HomeSpider(CrawlSpider):
    name = 'home1'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/shenzhen/ch90']
    hometype = ['g32704', 'g25475', 'g33867', 'g33876', 'g34035', 'g6827', 'g6826', 'g32702', 'g32705']
    custom_settings = {
        'LOG_FILE': 'log_home1.txt',
    }

    def parse_start_url(self, response):
        for tp in self.hometype:
            for loc in dz_location[::-1]:
                baseurl = 'http://www.dianping.com/shenzhen/ch90/%s%s' % (tp, loc)
                yield Request(baseurl, callback=self.parse_list_first)

    def parse_list_first(self, response):
        maxpage = 0
        if response.css('.pageLink::text').extract():
            maxpage = int(response.css('.pageLink::attr(title)').extract()[-1])
            print('maxpage in first if: {}'.format(maxpage))
        elif response.css('.pages-num'):
            maxpage = 1
            print('maxpage in elif: {}'.format(maxpage))
        else:
            print('maxpage in else: {}'.format(maxpage))
        print('maxpage: {}'.format(maxpage))
        self.logger.debug('maxpage: {}'.format(maxpage))
        print('response.url: {}'.format(response.url))
        ul = response.url
        tp = ul.split('/')[-1].split('r')[0]
        for i in range(1, maxpage + 1):
            url = ul + 'p' + str(i)
            if tp in ['g25475', 'g32704']:
                print('tp in if : {}'.format(tp))
                yield Request(url, callback=self.parse_list_decoration)
            else:
                print('tp in else : {}'.format(tp))
                yield Request(url, callback=self.parse_list)

    def parse_list_decoration(self, response):
        item = HomeItem()

        div = response.css('.shop-list>.shop-list-item')
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
            item['district'] = i.css('.shop-location>span:first-child::text').extract_first()
            item['location'] = i.css('.shop-location>span:last-child::text').extract_first()
            if i.css('.shop-team').extract():
                item['design'] = i.css('.shop-team i:first-child::text').extract_first()
                item['designer'] = i.css('.shop-team i:last-child::text').extract_first()
            getlocation(item)
            item['number'] = item['url'].split('/')[-1]
            yield item

    def parse_list(self, response):
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
            item['review_num'] = int(i.css('.shop-info-text-i>a::text').re_first(r'[1-9]\d*|0'))
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
