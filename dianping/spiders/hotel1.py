# -*- coding: utf-8 -*-
import json
import re

from scrapy.spiders import CrawlSpider
from scrapy import Request

from dianping.dz_location import dz_location, getlocation
from dianping.items import HotelItem


class HotelSpider(CrawlSpider):
    name = 'hotel1'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/shenzhen/hotel/']
    custom_settings = {
        'LOG_FILE': 'log_hotel1.txt',
    }

    def parse_start_url(self, response):
        for loc in dz_location[::]:
            baseurl = 'http://www.dianping.com/shenzhen/hotel/%s' % loc
            yield Request(baseurl, callback=self.parse_list_first)

    def parse_list_first(self, response):
        #### 获取分页
        maxpage = 0
        if response.css('.page .next'):
            # maxpage = int(e('.PageLink:last').attr('data-ga-page'))
            maxpage = int(response.css('.page a::text').extract()[-2])
        elif len(response.css('.page a').extract()) == 1:
            maxpage = 1
        else:
            print('maxpage in else: {}'.format(maxpage))
        print('maxpage: {}'.format(maxpage))
        self.logger.debug('maxpage: {}'.format(maxpage))
        print('response.url ' + response.url)
        baseurl = str(response.url)
        for i in range(maxpage, 0, -1):
            url = baseurl + 'p' + str(i)
            yield Request(url, callback=self.parse_list)
            # hotel = hotel_from_url_json(url)

        # pages = selector.xpath('//div[@class="page"]/a/@data-ga-page').extract()
        #
        # if len(pages) > 0:
        #     pg = pages[len(pages) - 2]
        # pg=int(str(pg))+1
        # url = str(response.url)
        #
        # for p in range(1,pg):
        #     ul = url+'p'+str(p)
        #
        #     yield Request(ul,callback=self.parse_list)

    def parse_list(self, response):
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
            item['pic_array'] = record.get('picArray')
            getlocation(item)
            yield item
