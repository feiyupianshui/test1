#!/use/bin/env python
#_*_coding:utf-8_*_
import scrapy
from scrapy.spider import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor
from scrapy import FormRequest
from bs4 import BeautifulSoup
from radiowave.items import RadiowaveItem


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
        item = RadiowaveItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find('h1', class_="entry-title h3").get_text()
        category = response.url.split('/')[-2]
        dramaname = name.split('电波字幕组')[0]
        dramaid = response.url.split('.html')[0].split('/')[-1]
        item['dramaname'] = dramaname
        item['category'] = category
        item['dramapage'] = response.url
        item['dramaid'] = response.url.split('.html')[0].split('/')[-1]

        imgurltag = soup.find('img', class_="alignnone")
        if imgurltag is None:
            print('图片不存在')
            item['imgurl'] = '图片不存在'
        else:
            item['imgurl'] = imgurltag['src']

        return item
