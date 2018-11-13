# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider

from dianping.dz_location import dz_location, getlocation
from dianping.items import ShoppingItem


class ShoppingSpider(CrawlSpider):
    name = 'shopping1'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/shenzhen/ch20']
    shoppingtype = ['g120', 'g33943', 'g33944', 'g33906', 'g33905', 'g33904', 'g119', 'g122', 'g121', 'g130', 'g32739',
                    'g187', 'g235', 'g123', 'g128', 'g125', 'g27809', 'g27810', 'g27811', 'g27812', 'g26085', 'g124',
                    'g127', 'g126', 'g6826', 'g32705', 'g6829', 'g6827', 'g32700', 'g6830', 'g34124', 'g129', 'g184',
                    'g33760', 'g33759', 'g2714', 'g26101', 'g33858', 'g2776', 'g32698', 'g34114', 'g131']
    custom_settings = {
        'LOG_FILE': 'log_shopping1.txt',
    }
    def parse_start_url(self, response):
        for tp in self.shoppingtype:
            for loc in dz_location[::-1]:
                baseurl = 'http://www.dianping.com/shenzhen/ch20/%s%s' % (tp, loc)
                # self.logger.debug('baseurl ' + baseurl)
                yield Request(baseurl, callback=self.parse_list_first)

    def parse_list_first(self, response):
        maxpage = 0
        if response.css('.PageLink::text').extract():
            maxpage = int(response.css('.PageLink::attr(data-ga-page)').extract()[-1])
        elif 0 < len(response.css('#shop-all-list li')) <= 15:
            maxpage = 1
        else:
            print('maxpage in else: {}'.format(maxpage))
        print('maxpage: {}'.format(maxpage))
        self.logger.debug('maxpage: {}'.format(maxpage))
        print('response.url ' + response.url)
        ul = str(response.url)
        for i in range(1, maxpage + 1):
            url = ul + 'p' + str(i)
            yield Request(url, callback=self.parse_list)

    def parse_list(self, response):
        item = ShoppingItem()

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
            # else:
            #     item['mean_price'] = '-'
            print('1111111 quality environment service: {}'.format(i.css('.comment-list b::text').extract()))
            if i.css('.comment-list b::text').extract():
                print('222222 quality environment service: {}'.format(i.css('.comment-list b::text').extract()))
                item['quality'] = float(i.css('.comment-list b::text').extract()[0])
                item['environment'] = float(i.css('.comment-list b::text').extract()[1])
                item['service'] = float(i.css('.comment-list b::text').extract()[2])
            print('type location 1: {}'.format(i.css('.tag-addr span::text').extract()))
            item['type'] = i.css('.tag-addr span::text').extract()[0].strip()
            item['location'] = i.css('.tag-addr span::text').extract()[1].strip()
            item['address'] = i.css('.addr::text').extract_first().strip()
            getlocation(item)
            item['number'] = item['url'].split('/')[-1]
            yield item
