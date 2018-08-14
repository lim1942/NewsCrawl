# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Xinxinlvyou_lvyouzixunSpider(CrawlSpider):
    
    IR_SITENAME = '欣欣旅游'
    CHANNAL_PATH  ='旅游资讯'
    DOCCHANNEL = '旅游资讯'
    name = 'xinxinlvyou_lvyouzixun'
    # allowed_domains = ['''']
    start_urls = ['http://news.cncn.com/yunnan/']
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="news_list"]/li/a'), callback='parse_item'),
    )

    def parse_start_url(self,response):
        item =  {}
        indexLen = len(response.xpath('//ul[@class="news_list"]/li/a').extract())
        item['indexLen'] = indexLen
        return item

    def parse_item(self, response):
        item =  {}
        item['url'] = response.request.url


        item['title'] = response.xpath('//div[@class="news_con"]/h1').extract_first()
        item['content'] = response.xpath('//div[@class="con"]/@class').extract_first()
        item['source'] = response.xpath('//div[@class="time"]/span/@class').extract_first()
        item['author'] = ''
        item['time'] = response.xpath('//div[@class="time"]/@class').extract_first()
        item['topTitle'] = ''
        item['bottomTitle'] = ''
        return item