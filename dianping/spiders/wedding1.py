# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider

from dianping.dz_location import dz_location, getlocation
from dianping.items import WeddingItem


class WeddingSpider(CrawlSpider):
    name = 'wedding1'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/shenzhen/ch55']
    weddingtype = ['g25410', 'g33888', 'g34057', 'g163', 'g162', 'g167', 'g191', 'g166', 'g185', 'g6700', 'g164',
                   'g25412', 'g186', 'g192', 'g6844']
    custom_settings = {
        'LOG_FILE': 'log_wedding1.txt',
    }
    def parse_start_url(self, response):
        for tp in self.weddingtype:
            for loc in dz_location[::-1]:
                baseurl = 'http://www.dianping.com/shenzhen/ch55/%s%s' % (tp, loc)
                yield Request(baseurl, callback=self.parse_list_first)

    def parse_list_first(self, response):
        maxpage = 0
        if response.css('.PageLink::text').extract():
            maxpage = int(response.css('.PageLink::attr(title)').extract()[-1])
        elif 0 < len(response.css('.shop-list li')) <= 15:
            maxpage = 1
        else:
            print('maxpage in else: {}'.format(maxpage))
        print('maxpage: {}'.format(maxpage))
        print('response.url: {}'.format(response.url))
        ul = response.url
        for i in range(1, maxpage + 1):
            url = ul + 'p' + str(i)
            yield Request(url, callback=self.parse_list)

    def parse_list(self, response):
        item = WeddingItem()

        li = response.css('.shop-list>li')
        print('parse_list li:{}  response.url: {}'.format(li.css('.shopname::text').extract(), response.url))
        self.logger.debug('parse_list li:{}  response.url: {}'.format(li.css('.shopname::text').extract(), response.url))
        for i in li:
            item['title'] = i.css('.shopname::text').extract_first()
            item['url'] = 'http:' + i.css('.shopname::attr(href)').extract_first()
            if i.css('a img::attr(data-lazyload)').extract_first():
                item['img'] = 'http:' + i.css('a img::attr(data-lazyload)').extract_first()
            else:
                item['img'] = 'http:' + i.css('a img::attr(src)').extract_first()
            item['star'] = float(i.css('.item-rank-rst::attr(class)').re_first(r'[1-9]\d*|0')) / 10
            item['review_num'] = i.css('p.remark > span:nth-child(2) > a::text').re_first(r'[1-9]\d*|0')
            item['mean_price'] = i.css('.price::text').extract_first()
            item['product_photos'] = i.css('p.remark > span:nth-child(3) > a::text').extract_first()
            if i.css('.area-list::text').extract_first():
                item['location'] = ' '.join(i.css('.area-list::text').extract_first().strip().split())
            else:
                item['location'] = ''
            getlocation(item)
            item['number'] = item['url'].split('/')[-1]
            yield item
