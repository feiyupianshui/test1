#!/use/bin/env python
#_*_coding:utf-8_*_
import scrapy
from scrapy.spider import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor
from scrapy import FormRequest
from bs4 import BeautifulSoup

account = 'Q8B1948D90565EAA8F705E7C91E4CAAE6'
password = '^118667'

class myspider(CrawlSpider):
    name = 'test1'
    allowed_domain = ['dbfansub.com']
    start_urls = ['http://dbfansub.com/user/login/?redirect_to=http%3A%2F%2Fdbfansub.com%2Ftvshow%2F8902.html']

    def parse_start_url(self, response):
        formdata = {
            'log': 'Q8B1948D90565EAA8F705E7C91E4CAAE6',
            'pwd': '^118667',
            'wp-submit': '登录',
            'redirect_to': 'http://dbfansub.com/tvshow/8902.html',
            'testcookie': '1'
        }
        return [FormRequest.from_response(response, formdata=formdata, callback=self.after_login)]

    def after_login(self,response):
        lnk = 'http://dbfansub.com/'
        return Request(lnk)

    rules = (
        Rule(LinkExtractor(allow=('\.html',), deny =('weibo','qq','redirect','login',)), callback = 'parse_item', follow=True),
    )

    def parse_item(self,response):
        print(response.url)
        pass
