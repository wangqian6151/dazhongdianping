# -*- coding: utf-8 -*-
import re

from scrapy.spiders import CrawlSpider
from scrapy import Request
from dianping.dz_location import dz_location, getlocation
from dianping.items import ServiceItem


class ServiceSpider(CrawlSpider):
    name = 'service1'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/shenzhen/ch80']
    servicetype = ['g195',
                   # 家政
                   'g2928',
                   # 生活配送
                   'g836', 'g26465', 'g26466', 'g33970', 'g34028', 'g34029', 'g34017',
                   # 房屋地产
                   'g33971', 'g26085', 'g181', 'g835', 'g182', 'g33972', 'g3063', 'g33975', 'g33973', 'g612', 'g33974',
                   'g32753',
                   # 便民服务
                   'g34003', 'g237', 'g34004', 'g34005', 'g34006', 'g34007', 'g32721', 'g34008', 'g34009',
                   # 金融
                   'g33986', 'g32742', 'g2929',
                   # 搬家运输
                   'g3064',
                   # 快照摄影
                   'g3066', 'g34001', 'g34000', 'g34002',
                   # 文印图文
                   'g33762',
                   # 洗涤护理
                   'g33958',
                   # 商务服务
                   'g33976',
                   # 家电数码维修
                   'g33965',
                   # 文化传媒
                   'g26117',
                   # 居家维修
                   'g197',
                   # 旅行社
                   'g2930',
                   # 回收
                   'g979',
                   # 公司企业
                   'g980',
                   # 售票点
                   'g25462',
                   # 演出票务
                   'g6823',
                   # 交通
                   'g34031',
                   # 老年生活
                   'g34154',
                   #  心理咨询
                   'g2884',
                   # 商圈
                   'g3082',
                   # 政府机构
                   'g26119',
                   # 网站
                   'g34023',
                   # 情趣生活
                   'g33994', 'g26491'
                   ]
    custom_settings = {
        'LOG_FILE': 'log_service1.txt',
    }

    def parse_start_url(self, response):
        for tp in self.servicetype:
            for loc in dz_location[::-1]:
                baseurl = 'http://www.dianping.com/shenzhen/ch80/%s%s' % (tp, loc)
                yield Request(baseurl, callback=self.parse_list_first)

    def parse_list_first(self, response):
        maxpage = 0
        if response.css('.PageLink::text').extract():
            maxpage = int(response.css('.PageLink::attr(data-ga-page)').extract()[-1])
            # maxpage = int(response.css('.PageLink').eq(-1).attr('data-ga-page'))
        elif 0 < len(response.css('#shop-all-list li').extract()) <= 15:
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
        item = ServiceItem()

        li = response.css('#shop-all-list>ul>li')
        print('parse_list li:{}  response.url: {}'.format(li.css('.txt>.tit h4::text').extract(), response.url))
        self.logger.debug('parse_list li:{}  response.url: {}'.format(li.css('.txt>.tit h4::text').extract(), response.url))
        for i in li:
            item['title'] = i.css('.txt>.tit h4::text').extract_first().strip()
            item['url'] = i.css('.txt>.tit>a::attr(href)').extract_first()
            if i.css('.shop-branch::text'):
                item['branch'] = i.css('.shop-branch::attr(href)').extract_first()
            item['img'] = i.css('img::attr(data-src)').extract_first()
            # item['star'] = i.css('.sml-rank-stars::attr(title)').extract_first()
            item['star'] = float(
                re.search(r'[1-9]\d*|0', i.css('.sml-rank-stars::attr(class)').extract_first())[0]) / 10
            if i.css('.review-num b::text').extract_first():
                print('review-num : {}'.format(i.css('.review-num>b::text')))
                item['review_num'] = int(i.css('.review-num>b::text').extract_first())
            if i.css('.mean-price b::text'):
                item['mean_price'] = i.css('.mean-price b::text').extract_first().strip('￥')
                # item['mean_price'] = i.css('.mean-price b::text').extract_first().strip('￥')
            print('11111111 score environment service: {}'.format(i.css('.comment-list b::text').extract()))
            if i.css('.comment-list b::text').extract():
                print('2222222 score environment service: {}'.format(i.css('.comment-list b::text').extract()))
                item['score'] = float(i.css('.comment-list b::text').extract()[0])
                item['environment'] = float(i.css('.comment-list b::text').extract()[1])
                item['service'] = float(i.css('.comment-list span b::text').extract()[2])
            print('type location 1: {}'.format(i.css('.tag-addr span::text').extract()))
            # print('type location 2: {}'.format(i.css('.tag-addr span::text').extract()[0].strip()))
            # print('type location 3: {}'.format(i.css('.tag-addr span::text').extract()[1].strip()))
            item['type'] = i.css('.tag-addr span::text').extract()[0].strip()
            item['location'] = i.css('.tag-addr span::text').extract()[1].strip()
            item['address'] = i.css('.addr::text').extract_first().strip()
            getlocation(item)
            item['number'] = item['url'].split('/')[-1]
            yield item

    # def parse(self, response):
    #     pass
