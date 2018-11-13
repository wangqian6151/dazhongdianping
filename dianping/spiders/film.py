# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor

from dianping.dz_location import getlocation
from dianping.items import FilmItem


class Film2Spider(Spider):
    name = 'film'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/shenzhen/ch25']
    custom_settings = {
        'LOG_FILE': 'log_film.txt',
    }

    def parse(self, response):
        print('parse response.url:' + response.url)
        self.logger.debug('parse response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)

        le = LinkExtractor(restrict_css='#region-nav')
        print('1' * 50)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            # yield Request(link.url, callback=self.parse_list)
            yield Request(link.url, callback=self.parse_region)

    def parse_region(self, response):
        print('parse_region response.url:' + response.url)
        self.logger.debug('parse_region response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)

        le = LinkExtractor(restrict_css='#region-nav-sub')
        print('2' * 100)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            # yield Request(link.url, callback=self.parse_list)
            yield Request(link.url, callback=self.parse_classfy)

    def parse_classfy(self, response):
        print('parse_classfy response.url:' + response.url)
        self.logger.debug('parse_classfy response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='#classfy')
        print('3' * 150)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_list)

    def parse_list(self, response):
        print('parse_list response.url:' + response.url)
        self.logger.debug('parse_list response.url:' + response.url)
        item = FilmItem()

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
                item['mean_price'] = int(i.css('.mean-price b::text').extract_first().strip('￥'))
            print('type location 1: {}'.format(i.css('.tag-addr span::text').extract()))
            item['type'] = i.css('.tag-addr span::text').extract()[0].strip()
            item['location'] = i.css('.tag-addr span::text').extract()[1].strip()
            item['address'] = i.css('.addr::text').extract_first().strip()
            getlocation(item)
            item['number'] = item['url'].split('/')[-1]
            yield item

        le = LinkExtractor(restrict_css='div.page > a.next')
        print('4' * 200)
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            print('next_url:', next_url)
            self.logger.debug('parse_list next_url:{}'.format(next_url))
            yield Request(next_url, callback=self.parse_list)
