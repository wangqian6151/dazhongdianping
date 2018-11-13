# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider

from dianping.dz_location import dz_location, getlocation
from dianping.items import FoodItem


class FoodSpider(CrawlSpider):
    name = 'food1'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/shenzhen/ch10']
    # foodtype = ['g103', 'g205', 'g733', 'g1947', 'g32728', 'g1953', 'g111', 'g117', 'g1833', 'g241', 'g132', 'g113',
    #             'g33924', 'g225', 'g226', 'g34041', 'g34040', 'g110', 'g32731', 'g3027', 'g3023', 'g34060', 'g3017',
    #             'g4477', 'g32730', 'g208', 'g34061', 'g34063', 'g32729', 'g34065', 'g34062', 'g34064', 'g34066', 'g116',
    #             'g238', 'g24340', 'g254', 'g232', 'g231', 'g253', 'g219', 'g251', 'g508', 'g114', 'g102', 'g4467',
    #             'g4473', 'g4469', 'g115', 'g109', 'g104', 'g112', 'g210', 'g217', 'g1881', 'g221', 'g4509', 'g222',
    #             'g223', 'g4557', 'g118', 'g134', 'g133', 'g247', 'g246', 'g311', 'g6743', 'g1387', 'g26483', 'g26482',
    #             'g26484', 'g252', 'g34014', 'g101', 'g34055', 'g3243', 'g207', 'g106', 'g250', 'g34032', 'g1338',
    #             'g26481', 'g1959', 'g2714', 'g25474', 'g107', 'g34059', 'g1783']

    foodtype = ['g103', 'g111', 'g117', 'g132', 'g113', 'g110', 'g116', 'g219', 'g251', 'g508', 'g114', 'g102', 'g115',
                'g109', 'g104', 'g112', 'g118', 'g34014', 'g101', 'g34055', 'g3243', 'g207', 'g106', 'g250', 'g34032',
                'g1338', 'g26481', 'g1959', 'g2714', 'g25474', 'g107', 'g34059', 'g1783']
    custom_settings = {
        'LOG_FILE': 'log_food1.txt',
    }
    def parse_start_url(self, response):
        for tp in self.foodtype:
            for loc in dz_location[::-1]:
                baseurl = 'http://www.dianping.com/shenzhen/ch10/%s%s' % (tp, loc)
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
        item = FoodItem()

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
                print('review-num : {}'.format(i.css('.review-num>b::text')))
                item['review_num'] = int(i.css('.review-num>b::text').extract_first())
            if i.css('.mean-price b::text'):
                item['mean_price'] = i.css('.mean-price b::text').extract_first().strip('￥')
            # else:
            #     item['mean_price'] = '-'
            print('1111111 taste environment service: {}'.format(i.css('.comment-list b::text').extract()))
            if i.css('.comment-list b::text').extract():
                print('222222 taste environment service: {}'.format(i.css('.comment-list b::text').extract()))
                item['taste'] = float(i.css('.comment-list b::text').extract()[0])
                item['environment'] = float(i.css('.comment-list b::text').extract()[1])
                item['service'] = float(i.css('.comment-list b::text').extract()[2])
            if i.css('div.txt > div.recommend'):
                print("i.css('div.txt > div.recommend a') : {}".format(
                    i.css('div.txt > div.recommend a::text').extract()))
                item['recommend'] = ' '.join(i.css('div.txt > div.recommend a::text').extract())
            print('type location 1: {}'.format(i.css('.tag-addr span::text').extract()))
            item['type'] = i.css('.tag-addr span::text').extract()[0].strip()
            item['location'] = i.css('.tag-addr span::text').extract()[1].strip()
            item['address'] = i.css('.addr::text').extract_first().strip()
            getlocation(item)
            item['number'] = item['url'].split('/')[-1]
            yield item
