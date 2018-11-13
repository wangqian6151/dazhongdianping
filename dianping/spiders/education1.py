# -*- coding: utf-8 -*-
import scrapy

from scrapy import Request
from scrapy.spiders import CrawlSpider

from dianping.dz_location import dz_location, getlocation
from dianping.items import EducationItem


class EducationSpider(CrawlSpider):
    name = 'education1'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/shenzhen/ch75']
    educationtype = ['g2872', 'g2873', 'g2877', 'g2876', 'g2874', 'g2878', 'g179', 'g260', 'g32722', 'g34105', 'g33897',
                     'g33899', 'g33898', 'g34106', 'g34107', 'g2882']
    custom_settings = {
        'LOG_FILE': 'log_education1.txt',
    }

    def parse_start_url(self, response):
        for tp in self.educationtype:
            for loc in dz_location[::-1]:
                baseurl = 'http://www.dianping.com/shenzhen/ch75/%s%s' % (tp, loc)
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
        item = EducationItem()

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
            print('1111111 effect teachers environment: {}'.format(i.css('.comment-list b::text').extract()))
            if i.css('.comment-list b::text').extract():
                print('222222 effect teachers environment: {}'.format(i.css('.comment-list b::text').extract()))
                item['effect'] = float(i.css('.comment-list b::text').extract()[0])
                item['teachers'] = float(i.css('.comment-list b::text').extract()[1])
                item['environment'] = float(i.css('.comment-list b::text').extract()[2])
            print('type location 1: {}'.format(i.css('.tag-addr span::text').extract()))
            item['type'] = i.css('.tag-addr span::text').extract()[0].strip()
            item['location'] = i.css('.tag-addr span::text').extract()[1].strip()
            item['address'] = i.css('.addr::text').extract_first().strip()
            getlocation(item)
            item['number'] = item['url'].split('/')[-1]
            yield item
