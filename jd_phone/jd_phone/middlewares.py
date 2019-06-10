# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import requests
import re
import json
from selenium import webdriver
import time


class JdPhoneSpiderMiddleware(object):
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


class JdPhoneDownloaderMiddleware(object):
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

class RandomHeaderMiddleware(object):
    def __init__(self):
        self.headers = [
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13",
            "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:2.0) Treco/20110515 Fireweb Navigator/2.4",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Flock/3.5.3.4628 Chrome/7.0.517.450 Safari/534.7",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko/20090327 Galeon/2.0.7",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)",
            "Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)"
        ]

    def process_request(self,request,spider):
        request.headers["User-Agent"]=random.choice(self.headers)


class RandomProxyMiddleware(object):
    def __init__(self):
        self.proxies = [
            'http://58.218.200.249:4386', 'http://58.218.200.247:4031', 'http://58.218.200.247:9152', 'http://58.218.200.237:2903', 'http://58.218.200.248:6209', 'http://58.218.200.229:4096', 'http://58.218.200.249:3959', 'http://58.218.200.247:4007', 'http://58.218.200.229:7520', 'http://58.218.200.229:7993', 'http://58.218.200.237:4401', 'http://58.218.200.247:7827', 'http://58.218.200.248:4089', 'http://58.218.200.229:5382', 'http://58.218.200.249:4957', 'http://58.218.200.248:8326', 'http://58.218.200.229:3915', 'http://58.218.200.229:7026', 'http://58.218.200.229:6671', 'http://58.218.200.248:9058', 'http://58.218.200.248:4760', 'http://58.218.200.229:6839', 'http://58.218.200.249:8542', 'http://58.218.200.249:4314', 'http://58.218.200.229:8977', 'http://58.218.200.229:3565', 'http://58.218.200.249:4954', 'http://58.218.200.229:4826', 'http://58.218.200.237:4400', 'http://58.218.200.248:3237', 'http://58.218.200.247:7592', 'http://58.218.200.249:7169', 'http://58.218.200.249:7792', 'http://58.218.200.229:3913', 'http://58.218.200.247:3222', 'http://58.218.200.247:3669', 'http://58.218.200.237:6500', 'http://58.218.200.237:3457', 'http://58.218.200.237:8544', 'http://58.218.200.237:2601', 'http://58.218.200.248:5419', 'http://58.218.200.248:3752', 'http://58.218.200.237:6380', 'http://58.218.200.248:5538', 'http://58.218.200.249:8789', 'http://58.218.200.248:2347', 'http://58.218.200.248:9126', 'http://58.218.200.249:9031', 'http://58.218.200.249:6798', 'http://58.218.200.247:2446'
        ]
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        }

    def process_response(self,request,response,spider):
        proxy = random.choice(self.proxies)
        if response.status!=200:
            request.meta["proxy"]=proxy
            print("本次使用的代理是",proxy)
            self.proxies.remove(proxy)
            return request
        return response