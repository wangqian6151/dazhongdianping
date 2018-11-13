# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

import time
import random
import logging
from scrapy import signals
import base64
from fake_useragent import UserAgent

from dianping.dz_location import cookies2dict

ua = UserAgent()
# 代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
proxyUser = "H01234567890123D"
proxyPass = "0123456789012345"

# # for Python2
# proxyAuth = "Basic " + base64.b64encode(proxyUser + ":" + proxyPass)


# for Python3
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer

        request.headers["Proxy-Authorization"] = proxyAuth


class TooManyRequestsRetryMiddleware(RetryMiddleware):

    def __init__(self, crawler):
        super(TooManyRequestsRetryMiddleware, self).__init__(crawler.settings)
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        elif response.status == 429:
            self.crawler.engine.pause()
            time.sleep(60)  # If the rate limit is renewed in a minute, put 60 seconds, and so on.
            self.crawler.engine.unpause()
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        elif response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response


class RandomUserAgentMiddleware(object):
    def __init__(self):
        self.user_agents = []
        self.logger = logging.getLogger(__name__)

    def process_request(self, request, spider):
        useragent = ua.random
        print('User-Agent:' + useragent)
        self.logger.debug('User-Agent:' + useragent)
        request.headers['User-Agent'] = useragent


class RandomCookiesMiddleware(object):
    def __init__(self):
        self.cookies = [
            'cy=7; cye=shenzhen; _lxsdk_cuid=1656a48048bc8-0fe86f7951e859-4c312b7b-1fa400-1656a48048b45; _lxsdk_s=1656a48048d-031-39d-43f%7C%7C26; _lxsdk=1656a48048bc8-0fe86f7951e859-4c312b7b-1fa400-1656a48048b45; _hc.v=614b63ec-9574-aac5-b0e0-6bcc3b9f4728.1535086429; dper=a5f999d82ca0e3f79e667c1607d1c67fe506f830beba2d23380fa6ef018fc6a156a7b1821ba00ea4a5736d5cc67ca7950dfc1a4938237df828b54a4653fa96a1e46a1858d44c0ed102cafa2d7414ed771490c28d0e54ab7effb91e36ee703762; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_69178432071; ctu=cf30eb3a2208bf59e731f2c124c569b0e49fc1a66f16617cd10bbc4fef614a35; uamo=18603012947',
            'cy=7; cye=shenzhen; _lxsdk_cuid=1656a38c92833-057d6798253db4-784a5037-1fa400-1656a38c929c8; _lxsdk_s=1656a38c92a-0b-519-ce8%7C%7C29; _lxsdk=1656a38c92833-057d6798253db4-784a5037-1fa400-1656a38c929c8; _hc.v=7373b553-5d7e-165d-ef3c-08b8787f0349.1535085431; dper=2ff76984d85daed551ed81261950e8e12fc4b2d987a433fac853aae290b8ca016317c3b6e73591e9fc3a24233a173f9a0b5813564d98408b9ad0959c0fcb65fc67f161e504e1c792bd05fe1ec6eee135c34c5cbb5ba2c05c317e58e65039bbfc; ll=7fd06e815b796be3df069dec7836c3df; ua=18312529671; ctu=5b6309d42a05ae4dd213481415b102b4d50d5b6d229dfd60a8acb9d37609be89',
            '_lxsdk_cuid=163dcf4d2f3c8-0183cdb3d20aca-5e4b2519-1fa400-163dcf4d2f3c8; _lxsdk=163dcf4d2f3c8-0183cdb3d20aca-5e4b2519-1fa400-163dcf4d2f3c8; _hc.v=4b138761-b7c0-a8ad-c357-a6dd990451c1.1528420422; s_ViewType=10; ctu=5b6309d42a05ae4dd213481415b102b41b10ffbde57840e084f7ee09eab0b8cb; aburl=1; Hm_lvt_4c4fc10949f0d691f3a2cc4ca5065397=1528971283,1530176708,1530950732; __mta=214923560.1528964249753.1531124184220.1531129100944.124; _dp.ac.v=41b6401b-c777-4eba-9ea3-6d7709a3976f; __utmz=1.1532048721.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); QRCodeBottomSlide=hasShown; __utma=1.803687495.1532048721.1532048721.1533809958.2; _adwp=169583271.2320216919.1534476513.1534476513.1534476513.1; cy=7; cye=shenzhen; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1533626865,1534728563,1534995834; wed_user_path=2818|0; Hm_lpvt_dbeeb675516927da776beeb1d9802bd4=1535072079; lgtoken=025ee68ab-211a-4590-91bc-e099754fa22f; dper=12648f0f54f5d8703da385e59e5769bb15efdf6950309b8fb823a2e2e3a947f68370059032b09279812b7542d526e816a96e7f31c0cdb9867bf0c2cc1dd359f456cae40f603c51bb7b2b6304abcc8a7f405b5547e4b293ed2024e4a68c6131c5; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_2460430632; uamo=15012603932; _lxsdk_s=1656a3d24c7-3e-b1-5ea%7C%7C27',
            'cy=7; cye=shenzhen; _lxsdk_cuid=1656a3e20fac8-02c7e38ce15b0a-6b111b7e-1fa400-1656a3e20fac8; _lxsdk=1656a3e20fac8-02c7e38ce15b0a-6b111b7e-1fa400-1656a3e20fac8; _hc.v=198fd392-e554-669b-1823-5d3fde726ef5.1535085782; lgtoken=0dbab86d8-8cbe-4e1e-9aef-638366277401; dper=5f99c6ab1b74572017f7c31799d57f8a967553889c2bf0a1ded35dd1f5b8b3b165893d3c200dec90d70f2d9433c689156c22b4480737a830a3e0758733697e47e41a3ac6697b46928957bb5ddae5b6391462c1afb631f1f0e16916d7c438ff96; ll=7fd06e815b796be3df069dec7836c3df; ua=15200730164; ctu=068b5cc7e339b23a8684d9a2bf474d58c46d0ee51bb1b6919d4a64a417ffa18b; _lxsdk_s=1656a3e20fb-d94-707-8d2%7C%7C21',
            's_ViewType=10; _lxsdk_cuid=164fd78b3c7c8-032136437f5367-3c604504-1fa400-164fd78b3c759; _lxsdk=164fd78b3c7c8-032136437f5367-3c604504-1fa400-164fd78b3c759; _hc.v=65b59ff0-f78a-4568-8369-c36ea82acb80.1533260904; __mta=43375258.1533283022314.1533283022314.1533283022314.1; aburl=1; cy=7; cye=shenzhen; QRCodeBottomSlide=hasShown; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1533691963,1534294019,1534407669,1534820180; m_flash2=1; cityid=7; default_ab=index%3AA%3A1; switchcityflashtoast=1; _tr.u=tEbOR9P9Cc6zPhNB; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; dper=e180cb2cf7d577604dbb06239a1925b921e101d8208e2149c31871465d4acfe61efb25fc1805df3ed86fed7e02770bb26976e4ae8bf445ccfc5f7da529327a6a64528e3f33d8344db36187c42e19f88311a4cd9702cab54c7677769d458d0495; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_5837056877; ctu=72a908e858ecffe2fa4d2dce5752da13a068a7f46a3bd3cc1284ba47d6e75c9e; uamo=13048905567; _lxsdk_s=1656a3f9e21-7d1-ac6-cac%7C%7C98'

            #     'uamo=18312529671; _hc.v=189ee497-f45e-1164-648f-48ae8571b6e4.1531304312; ctu=5b6309d42a05ae4dd213481415b102b4b1c4c0ac0443e489402f03016e53d50d; _lxsdk_cuid=16488d97e71c8-04b82251d8a779-784a5037-1fa400-16488d97e72c8; _lxsdk=16488d97e71c8-04b82251d8a779-784a5037-1fa400-16488d97e72c8; ua=wangqian6151; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; cye=shenzhen; _lxsdk_s=164ab477cc9-0a2-51b-f1c%7C%7C43; cy=7; lgtoken=0b9a40890-9d88-44ab-87aa-292c1a66f571; dper=ccab61fe549d84a8f4e11374b614ba650fe038f0e99e0637232f076ed78fb0b1d7287af4934c308d8d109722b03db5c8f1db87d2901503e14b11e5431fd7c88a66ef1d8a610796e7eecd5f7312f91fc68123d608f67990a97d5aa87581c5267c; ll=7fd06e815b796be3df069dec7836c3df; ctu=a128b8ba9b1f9c7f5c3151a5c407c42f42cb62f856b71604cc7f241c3648f7f076e7934256734e27cc0b5b8ceaebf473',
            #     'cye=shenzhen; _lxsdk_cuid=163dcf4d2f3c8-0183cdb3d20aca-5e4b2519-1fa400-163dcf4d2f3c8; _lxsdk=163dcf4d2f3c8-0183cdb3d20aca-5e4b2519-1fa400-163dcf4d2f3c8; _hc.v=4b138761-b7c0-a8ad-c357-a6dd990451c1.1528420422; s_ViewType=10; ctu=5b6309d42a05ae4dd213481415b102b41b10ffbde57840e084f7ee09eab0b8cb; aburl=1; cy=7; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1530066838,1530517916,1530588829,1530868655; cy=7; cityid=7; cye=shenzhen; Hm_lvt_4c4fc10949f0d691f3a2cc4ca5065397=1528971283,1530176708,1530950732; Hm_lpvt_4c4fc10949f0d691f3a2cc4ca5065397=1530950732; lastVisitUrl=%2Fshenzhen%2Fhotel%2Fr31; __mta=214923560.1528964249753.1531124184220.1531129100944.124; thirdtoken=9A26A175B640CF8C437D0290137C0760; JSESSIONID=B9857D9A439B375F8ACF8F93041E9AC6; bind_feed=Sina; _dp.ac.v=41b6401b-c777-4eba-9ea3-6d7709a3976f; Hm_lpvt_dbeeb675516927da776beeb1d9802bd4=1531356479; uamo=15012603932; ctu=986f8347443b5584c2cc3e784eb6caad52244495290d1d3e56fea31bc737b689dca3b622f93681987341fd532fe4aeb0; catBrowserName=catBrowserValue; apollo-agent-pc-static-user-lonin-cookie-time-oneDay=Tue%20Jul%2017%202018%2018:00:03%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4); lgtoken=0a175ae63-7510-45c3-9377-3d7d48d1b127; dper=5f99c6ab1b74572017f7c31799d57f8a88cef35d61fbf99b2e6506169d7213034fbaaddf2c7870909b080c81bf82d214868a85ab37d860b84e87fa34323ca04ce734639416315badb9196c9025f5b67412c08e8125832e0086b9e110de64004f; ll=7fd06e815b796be3df069dec7836c3df; ua=15200730164; _lxsdk_s=164ab4a3fe5-311-90a-345%7C%7C13',
            #     'cy=7; cye=shenzhen; _lxsdk_cuid=1648c1b10b9c8-050881ab1e64f8-3351427c-1fa400-1648c1b10b944; _lxsdk=1648c1b10b9c8-050881ab1e64f8-3351427c-1fa400-1648c1b10b944; _hc.v=590d7836-b4f0-1060-da20-92b1c3fa0954.1531358942; _dp.ac.v=7e331984-7611-4c67-a3ab-0995c8a0d548; ctu=3b0560417a4dd025ae35ec69dafae5b53d752b6ef4b8d7a300e6d2b19a83cdf4; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; ctu=c014b184cb4be38a7ec7abf02ffeb91f2cd21e10d84bf2da3957eb2e9f21741580457dad7d86647c231718de2db65ba5; dper=e180cb2cf7d577604dbb06239a1925b9345be954de2df08a19aa7c3f2c2b24e005d478616818cfe495d96e0a2d2653ea243477d31065d69a6fcd7b99ac821dc714345a4f878ef477a70618f7d4b93c4b93ff9bfa1c9eb42a24999994d62982cd; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_5837056877; uamo=13048905567; _lxsdk_s=164ab4e37fd-7a0-6e0-639%7C%7C48',
            #     'cy=7; cye=shenzhen; _lxsdk_cuid=16488d3fcd69-0ef7d447345ba18-4c312b7b-1fa400-16488d3fcd7c8; _lxsdk=16488d3fcd69-0ef7d447345ba18-4c312b7b-1fa400-16488d3fcd7c8; _hc.v=72331155-2353-253c-3bc4-3df4ada336ef.1531303952; ua=dpuser_2460430632; ctu=068b5cc7e339b23a8684d9a2bf474d58ef6054778b51d575544cf4a7af3994ee; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; ctu=81b521e8c94606b4281a32d4bbab10487611da4f276f9298eba0af9a7f348644cecc62600a1bc355fc66476b6f6f15ff; _lxsdk_s=164ab51f388-d3d-0d0-15e%7C%7C23; lgtoken=05b1be2be-5c3e-4a9a-9340-235dd5c9a04b; dper=12648f0f54f5d8703da385e59e5769bbb19212f9aac92eb8f33864b9389f5af8f2d0f1c53bae5ab60b28903581c17ac5133c8e1ce6b89b137b4069bc912368e07d5df895a2c94693dc1a68a129a26a2ac9929a012b584f3fe2137cf6c73cee05; ll=7fd06e815b796be3df069dec7836c3df; uamo=15012603932',
            #     'cy=7; cye=shenzhen; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=1648c1e5eb27-0b23c592533ba6-61231d53-1fa400-1648c1e5eb3c8; _lxsdk=1648c1e5eb27-0b23c592533ba6-61231d53-1fa400-1648c1e5eb3c8; _hc.v=26340449-dc9c-7c12-18a7-87ae84c15df7.1531359158; ctu=cf30eb3a2208bf59e731f2c124c569b02d322e3e888bac4670646dc26b28776e; s_ViewType=10; cityInfo=%7B%22cityId%22%3A7%2C%22cityEnName%22%3A%22shenzhen%22%2C%22cityName%22%3A%22%E6%B7%B1%E5%9C%B3%22%7D; lastVisitUrl=%2Fshenzhen%2Fhotel%2Fr12036; selectLevel=%7B%22level1%22%3A%222%22%7D; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1531710699; Hm_lpvt_dbeeb675516927da776beeb1d9802bd4=1531710810; __mta=21426948.1531710700162.1531710700162.1531710810487.2; ctu=2bd1431edf381eaa9ad290f1c2cf6b8e81dde1f953989171ca62396a21815a4eb690546bcc312943b61652e3fc00c2d5; lgtoken=0abf73723-c1b3-4dce-b6d3-c6d6ad67ff1b; dper=6e6b885ec5f7076dd41202e43d50f6fae6be5688507b426187be71bb6c6b5202293b42323ea274a24a828f28d13be20f23db8519fb84c1a995c138db0309440c3c5c2909be1ea883123a3120a7fb8043d396adca5d202222d2901a40d10fe419; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_69178432071; uamo=18603012947; _lxsdk_s=164ab54feb5-6a8-6ec-c31%7C%7C22'
        ]
        self.logger = logging.getLogger(__name__)

    def process_request(self, request, spider):
        request.cookies = cookies2dict(random.choice(self.cookies))
        print('request.cookies: {}'.format(request.cookies))
        self.logger.debug('request.cookies: {}'.format(request.cookies))


class DianpingSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DianpingDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
