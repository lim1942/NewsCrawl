# -*- coding: utf-8 -*-
# @Author: lim
# @Date:   2018-08-13 13:52:04
# @Last Modified by:   xb12369
# @Last Modified time: 2018-08-20 15:31:30

import os
import re
import xlrd
from tools import get_pinyin ,excel_ensure



PATH = 'NewsCrawl/spiders/'
EXCEL_PATH = 'work/gen_spiders_from_excel/'
EXCEL_RESULT_PATH = 'work/gen_spiders_from_excel/result/'


TEMPLATE = """import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# 配置3个地方

class {}Spider(CrawlSpider):

    # 允许爬取的域名，可不配置
    # allowed_domains = [''''] 
    IR_SITENAME = '{}'
    CHANNAL_PATH  ='{}'
    DOCCHANNEL = '{}'
    name = '{}'
    start_urls = ['{}']
    
    # 1 >> 请配置概览页url提取规则，为了细缆页的爬取而配置的
    rules = (
        Rule(LinkExtractor(restrict_xpaths=""), callback='parse_item'),
    )

    def __init__(self, test=False, *args, **kwargs):
        super({}Spider, self).__init__(*args, **kwargs)
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
    command = ['scrapy','crawl','{}','-a','test=True']
    cmdline.execute(command)"""


def get_script_name(sitename,channel_path):
    sitename = sitename.replace('\\','').replace('/','')
    channel_path = channel_path.replace('\\','').replace('/','')
    word = sitename +'_' + channel_path
    script_name = re.sub(r'\W','',get_pinyin(word))
    if script_name[0].isdigit() or script_name[0] =='_':
        script_name = 'a_' + script_name
    return script_name



def get_spider_filename(name):
    filename = os.path.join(PATH,name+'.py')
    return filename



def gen_one_spider(sitename,channel_path,docchannel,weburl):
    name = get_script_name(sitename, channel_path)
    className = name[0].upper() + name[1:]
    filename = get_spider_filename(name)

    if os.path.exists(filename):
        print(sitename,channel_path,filename,'is already exists !!!')
        return

    processed_template = TEMPLATE.format(className,sitename,channel_path,docchannel,name,weburl,className,'{}','{}',name)
    with open(filename,'w',encoding='utf-8') as f:
        f.write(processed_template)

    print('successful gen',name,'for',sitename,channel_path)

    return True



def get_excel_filename():
    excel_con = []
    con = os.listdir(EXCEL_PATH)
    for i in con:
        if i.endswith('.xlsx'):
            excel_con.append(i)
    if len(excel_con)>1:
        print ('don`s push more than one excel in path')
        return
    if not excel_con:
        print('get none excel from path')
        return
    excel_filename = os.path.join(EXCEL_PATH,excel_con[0])
    return excel_filename



def gen_result(sitename,channel_path,docchannel,weburl,excel_filename):
    result_filename = os.path.join(EXCEL_RESULT_PATH,excel_filename.split('/')[-1].replace('xlsx','txt'))
    script_name = get_script_name(sitename,channel_path)
    line = '^'.join([script_name,sitename,channel_path,docchannel,weburl]) + '\n'
    with open(result_filename,'a',encoding='utf-8') as f:
        f.write(line)



def excel_is_alread_gen(excel_filename):
    name = excel_filename.split('/')[-1].replace('.xlsx','')
    result_list = os.listdir(EXCEL_RESULT_PATH)
    flag = True
    for res in result_list:
        if name in res:
            flag = False
    if flag:
        return excel_filename
    else:
        print('This excel has already gen,please check it out !!!')



def gen_spiders_from_excel():

    excel_filename = excel_ensure(get_excel_filename())
    excel_filename = excel_is_alread_gen(excel_filename)
    if not excel_filename:
        return

    r_file = xlrd.open_workbook(excel_filename)
    try:
        table = r_file.sheet_by_index(0)
    except Exception as e:
        print(e)

    if table.ncols != 4:
        print('Bad excel format, please check it out !!!  change it into 4 cols')
        return

    filter_rows = []
    for i in range(table.nrows):
        row  = table.row_values(i)
        if ('网站名' in row) and ('栏目名' in row):
            continue
        sitename = row[0]
        channel_path = row[1]
        docchannel = row[2]
        weburl = row[3]
        if gen_one_spider(sitename,channel_path,docchannel,weburl):
            gen_result(sitename,channel_path,docchannel,weburl,excel_filename)



if __name__ == '__main__':
    # gen_spiders_from_excel()
    gen_one_spider('39999健康网','资讯频道_食品安全','资讯频道_食品安全','http://news.39.net/ysbj/ys/test/')


