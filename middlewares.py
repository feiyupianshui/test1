# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import json
import redis
import random
from .useragent import agents
from .cookies import init_cookie#, remove_cookie, upadate_cookie这两个还没有定义
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware

class UserAgentmiddleware(UserAgentMiddleware):

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent

class CookieMiddleware(RetryMiddleware):#和内置的CookiesMiddleware不一样，而且是继承自重试中间件

    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)#这个操作叫重载，继承父类之后，子类是不能用 def init()方法的，不过重载父类之后就能用啦！
        self.rconn = redis.from_url(settings['REDIS_URL'], db=1, decode_responses=True)#最后的参数让取出的编码为str
        init_cookie(self.rconn, crawler.spider.name) #把cookie放入redis,crawler.spider.name是spidername的获取方法。

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)#访问settings

    def process_request(self, request, spider):
        redisKeys = self.rconn.keys()
        while len(redisKeys) > 0:
            elem random choice(redisKeys)
            if spider.name + ':Cookies' in elem:
                cookie = json.loads(self.rconn.get(elem))
                request.cookies = cookie
                request.meta['accountText'] = elem.split("Cookies:")[-1]
                break
            # else:
            #     redisKeys.remove(elem)

class Test1SpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
