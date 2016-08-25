# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 14:34:16 2016

@author: Administrator
"""

import scrapy
from sevevth.items import DmozItem
from scrapy.http import Request, FormRequest
#from scrapy.selector import Selector

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["www.qichacha.com"]
    start_urls = [
        "http://www.qichacha.com/",
           ]
    headers = {
        "Accept":"image/webp,image/*,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN,zh;q=0.8",    
        "Connection":"keep-alive",
        "Cookie":"cna=hmgbEAsrcEsCAXPDi3k/QFtI",
        "Host":"hm3.cnzz.com",
        "Referer":"http://www.qichacha.com/",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36 QIHU 360SE"
    }
    
    
    #land
    
    def start_requests(self):
        return [Request("http://www.qichacha.com/",  meta = {'cookiejar': 1}, callback = self.post_login)]

    def post_login(self, response):
            return [FormRequest.from_response(response,  
                                meta = {'cookiejar' : response.meta['cookiejar']},
                                dont_filter = True
                                )]
            
    
    def parse(self,response):
        
        for href in response.css("album > div.panel-body.m-t > div > div:nth-child(1) > section > div > div > a::attr('href')"):
            ##album > div.panel-body.m-t > div > div:nth-child(1) > section > div > div > a.text-black.text-lg
            url=response.urljoin(response.url,href.extract())
            #for url_cookie in enumerate(url):
            #yield scrapy.Request(url,meta = {cookie : i},callback=parse_main)
            yield scrapy.Request(url,callback=self.parse_middle)
    
    def parse_middle(self,response):
        for href_middle in response.css("body > div.container.m-t-md > div > div.col-md-8 > section > ul > a::attr('href')"):
            url_middle =response.css(response.url,href_middle.extract())
            #for url_cookie in enumerate(url_middle):
            #yield scrapy.Request(url,meta = {cookie : i},callback=parse_main)
            yield scrapy.Request(url_middle,callback=self.parse_main)

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
            item['introduce'] = sel_third.xpath('br/text()')
            yield item_ne
            