import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class A_39jiankangwang_zixunpindao_jiankangxinzhiSpider(CrawlSpider):
    
    IR_SITENAME = '39健康网'
    CHANNAL_PATH  ='资讯频道_健康新知'
    DOCCHANNEL = '资讯频道_健康新知'
    name = 'a_39jiankangwang_zixunpindao_jiankangxinzhi'
    # allowed_domains = ['''']
    start_urls = ['http://news.39.net/xinzhi/']
    rules = (
        Rule(LinkExtractor(restrict_xpaths="/html/body/div[@class='center_bottom']/ul[@class='center_left']/li/strong/a"), callback='parse_item'),
    )
    
    def __init__(self, test=False, *args, **kwargs):
        super(A_39jiankangwang_zixunpindao_jiankangxinzhiSpider, self).__init__(*args, **kwargs)
        self.test = test

    def parse_start_url(self,response):
        item =  {}
        indexLen = len(response.xpath("/html/body/div[@class='center_bottom']/ul[@class='center_left']/li/strong/a").extract())
        item['indexLen'] = indexLen
        return item

    def parse_item(self, response):
        item =  {}
        item['url'] = response.request.url


        item['title'] = response.xpath("/html/body/div[@class='center_bottom']/div[@class='sweetening']/div[@class='sweetening_title']/h1").extract_first()
        item['content'] = response.xpath("/html/body/div[@class='center_bottom']/div[@class='sweetening']/div[@id='contentText']").extract_first()
        item['source'] = ''
        item['author'] = ''
        item['time'] = response.xpath("/html/body/div[@class='center_bottom']/div[@class='sweetening']/div[@class='sweetening_title']/span[2]").extract_first()
        item['topTitle'] = ''
        item['bottomTitle'] = ''
        return item

if __name__ == '__main__':

    from scrapy import cmdline
    command = ['scrapy','crawl','a_39jiankangwang_zixunpindao_jiankangxinzhi','-a','test=True']
    cmdline.execute(command)
