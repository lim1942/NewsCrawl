import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# 配置3个地方

class A_39999jiankangwang_zixunpindao_shipinanquanSpider(CrawlSpider):

    # 允许爬取的域名，可不配置
    # allowed_domains = [''''] 
    IR_SITENAME = '39999健康网'
    CHANNAL_PATH  ='资讯频道_食品安全'
    DOCCHANNEL = '资讯频道_食品安全'
    name = 'a_39999jiankangwang_zixunpindao_shipinanquan'
    start_urls = ['http://news.39.net/ysbj/ys/test/']
    
    # 1 >> 请配置概览页url提取规则，为了细缆页的爬取而配置的
    rules = (
        Rule(LinkExtractor(restrict_xpaths=""), callback='parse_item'),
    )

    def __init__(self, test=False, *args, **kwargs):
        super(A_39999jiankangwang_zixunpindao_shipinanquanSpider, self).__init__(*args, **kwargs)
        self.test = test

    def parse_start_url(self,response):
        item =  {}

        # 2 >> 请配置概览页url提取规则(基本与1相同)，为了取概览页的内容而配置的
        indexLen = len(response.xpath("").extract())
        item['indexLen'] = indexLen
        return item

    def parse_item(self, response):
        item =  {}
        item['url'] = response.request.url

        # 3 >> 请配置细缆页字段提取规则
        item['title'] = response.xpath("").extract_first()
        item['content'] = response.xpath("").extract_first()
        item['source'] = response.xpath("").extract_first()
        item['author'] = response.xpath("").extract_first()
        item['time'] = response.xpath("").extract_first()
        item['topTitle'] = response.xpath("").extract_first()
        item['bottomTitle'] = response.xpath("").extract_first()
        return item

        

if __name__ == '__main__':

    from scrapy import cmdline
    command = ['scrapy','crawl','a_39999jiankangwang_zixunpindao_shipinanquan','-a','test=True']
    cmdline.execute(command)