import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class A_39jiankangwang_zixunpindao_quanweifabuSpider(CrawlSpider):
    
    IR_SITENAME = '39健康网'
    CHANNAL_PATH  ='资讯频道_权威发布'
    DOCCHANNEL = '资讯频道_权威发布'
    name = 'a_39jiankangwang_zixunpindao_quanweifabu'
    # allowed_domains = ['''']
    start_urls = ['http://news.39.net/qwfb/']
    rules = (
        Rule(LinkExtractor(restrict_xpaths="/html/body/div[@class='wrap'][2]/div[@class='con_left']/div[@class='listbox']/ul/li/span[@class='text']/a"), callback='parse_item'),
    )

    def parse_start_url(self,response):
        item =  {}
        indexLen = len(response.xpath("/html/body/div[@class='wrap'][2]/div[@class='con_left']/div[@class='listbox']/ul/li/span[@class='text']/a").extract())
        item['indexLen'] = indexLen
        return item

    def parse_item(self, response):
        item =  {}
        item['url'] = response.request.url


        item['title'] = response.xpath("/html/body/div[@id='art_box']/div[@class='art_left']/div[@class='art_box']/h1").extract_first()
        item['content'] = response.xpath("/html/body/div[@id='art_box']/div[@class='art_left']/div[@class='art_box']/div[@id='contentText']").extract_first()
        item['source'] = response.xpath("/html/body/div[@id='art_box']/div[@class='art_left']/div[@class='art_box']/div[@class='art_info']/div[@class='date']/em[2]/a").extract_first()
        item['author'] = ''
        item['time'] = response.xpath("/html/body/div[@id='art_box']/div[@class='art_left']/div[@class='art_box']/div[@class='art_info']/div[@class='date']").extract_first()
        item['topTitle'] = ''
        item['bottomTitle'] = ''
        return item