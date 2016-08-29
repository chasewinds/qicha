# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 14:34:16 2016

@author: Administrator
"""

import scrapy

from scrapy.http import Request, FormRequest
from sevevth.items import DmozItem
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["www.qichacha.com"]
    start_urls = [
        "http://www.qichacha.com/album_view_id_14640.shtml"
           ]
    headers = {
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Connection":"keep-alive",
        "Cookie":"grwng_uid=4d20a5a4-69d1-49b6-9a80-9dfbc06778b4; AWSELB=258D9D590E00B3DE939BD2301A2166BB8314D5BFDDB5C1F665452AFC91016E296945D3727C36EA43D6D89AD6C3DEFDDD64C09AED5DD08DC8FCD7CC530A4F473C260E3BA59502CF27597C7EC01453CCA5B5D1D0313D",
        "Host":"api.growingio.com",
        "Referer":"http://www.qichacha.com/album_view_id_14640.shtml",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"

               }

    def start_requests(self):
       return [Request("http://www.qichacha.com/album_view_id_14640.shtml",  meta = {'cookiejar': 1}, callback = self.post_login)]

    def post_login(self, response):
        return [FormRequest.from_response(response,
                                meta = {'cookiejar' : response.meta['cookiejar']},
                                callback = self.parse
                                )]

    
    def parse(self, response):
        print "parse..."
        #print response.body
        # body print successfully
        sel = Selector(response)
        print "befor xpath"
        for href in sel.xpath('/html/body/div/div').extract():
            url=response.urljoin(response.url,href.extract())
            print url
            yield Request
            yield scrapy.Request(url,callback=self.parse_middle)
    
    def parse_middle(self,response):
        print "in parse_middle"
        for href_middle in response.css("body > div.container.m-t-md > div > div.col-md-8 > section > ul > a:nth-child(1) > span.clear > span"):
            print "third"
            url_middle =response.css(response.url,href_middle.extract())
            #for i,url_cookie in enumerate(url_middle):               try to insert into cookie
            #yield scrapy.Request(url,meta = {cookie : i},callback=self.parse_main)
            print url_middle
            yield scrapy.Request(url_middle, callback=self.parse_main)

    def parse_main(self, response):
        print response.body
        for sel in response.xpath('//*[@id="company-top"]/div/div'):
            item_n = DmozItem()
            item_n['name'] = sel.xpath('span/span/text()').extract
            item_n['information'] = sel.xpath('span/small/text()').extract
            item_n['mail'] = sel.xpath('span/small/a/text()').extract
            yield item_n
            
        for sel_second in response.xpath('/html/body/div'):            
            item = DmozItem()
            item['title'] = sel_second.xpath('div/div/section/div/ul/li/lable/text()').extract()
            item['note'] = sel_second.xpath('div/div/section/div/ul/li/text()').extract()
            yield item
                        
        for sel_third in response.xpath('//*[@id="textShowMore"]'): 
            item_ne = DmozItem()
            item_ne['introduce'] = sel_third.xpath('br/text()')
            yield item_ne
            