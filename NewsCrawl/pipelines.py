# -*- coding: utf-8 -*-
# @Author: lim
# @Date:   2018-08-13 13:52:04
# @Last Modified by:   xb12369
# @Last Modified time: 2018-08-20 11:38:52

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import time

RESULT_ENCODING = 'utf-8'
UNCHECK_FILE_ENCODING = 'utf-8'


class NewscrawlPipeline(object):

    def __init__(self):  
        self.result = []
        self.start = time.time()
        self.o_start_time = self.get_datetime()
        self.path = os.path.join(os.path.dirname(os.path.dirname(
                    os.path.abspath(__file__))),'result')
        self.wrong_path = os.path.join(self.path,'wrong')


    def get_filename(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        filename = os.path.join(self.path,self.get_date_name())
        return filename


    def get_wrong_filename(self):
        if not os.path.exists(self.wrong_path):
            os.mkdir(self.wrong_path)
        wrong_filename = os.path.join(self.wrong_path,self.get_date_name())
        return wrong_filename


    def remove_success_from_uncheck_file(self,url):
        uncheck_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uncheck_filename = os.path.join(uncheck_file_path,'disable_script_list.txt')

        f = open(uncheck_filename,encoding=UNCHECK_FILE_ENCODING)
        lines = f.readlines()
        f.close()
        filter_con = ''
        for line in lines:
            if url not in line:
                filter_con += line
        with open(uncheck_filename,'w',encoding=UNCHECK_FILE_ENCODING) as f:
            f.write(filter_con)



    def get_date_name(self):
        return time.strftime('%Y-%m-%d') + '.txt'


    def get_datetime(self):
        return time.strftime('%H:%M:%S')


    def process_item(self, item, spider):
        self.result.append(item)
        return item


    def open_spider(self, spider):

        filename = self.get_filename()
        if not os.path.exists(filename):
            with open(filename,'w', encoding=RESULT_ENCODING) as f:
                field_head = ('脚本名^网站名^栏目名^栏目别名^网址^开始时间^用时^'
                             '首页检擦^标题^正文^来源^作者^时间^引题^副题^采集点评估\n')
                f.write(field_head)

        wrong_filename = self.get_wrong_filename()
        if not os.path.exists(wrong_filename):
            with open(wrong_filename,'w', encoding=RESULT_ENCODING) as f:
                wrong_field_head = ('网站名^栏目名^栏目别名^网址^首页检擦^标题^正文^来源^作者^时间^引题^副题\n')
                f.write(wrong_field_head)


    def close_spider(self, spider):

        SCRIPT_NAME = spider.name
        IR_SITENAME = spider.IR_SITENAME
        CHANNAL_PATH = spider.CHANNAL_PATH
        DOCCHANNEL = spider.DOCCHANNEL
        SITE_URL = spider.start_urls[0]
        START_TIME = self.o_start_time
        USE_TIME = str(int(time.time()-self.start)).split('.')[0]+'s'

        index = '' 
        title = ''
        content = ''
        source = ''
        author = ''
        _time = ''
        topTitle = ''
        bottomTitle = ''

        EVALUTE = ''

        # for just crawl index or not crawl
        if len(self.result)<=1:
            if len(self.result) == 0:
                EVALUTE = '概览页无响应' 
            else:
                indexLen = self.result[0].get('indexLen')
                index = '错误' if indexLen is None else '正常'
                EVALUTE ='细缆页无响应'

        # for crawl all page
        else:
            for item in self.result:
                if len(item) == 1:
                    indexLen = item.get('indexLen')
                    index = '错误' if indexLen is None else '正常'
                    continue

                url = item['url']

                if  item.get('title') is None:
                    title = url
                if  item.get('content') is None:
                    content = url
                if  item.get('source') is None:
                    source = url
                if  item.get('author') is None:
                    author = url
                if  item.get('time') is None:
                    _time = url
                if  item.get('topTitle') is None:
                    topTitle = url
                if  item.get('bottomTitle') is None:
                    bottomTitle = url

            title = '正常' if not title else '标题错误：'+title
            content = '正常' if not content else '内容错误：'+content
            source = '正常' if not source else '来源错误：'+source
            author = '正常' if not author else '作者错误：'+author
            _time = '正常' if not _time else '时间错误：'+_time
            topTitle = '正常' if not topTitle else '引题错误：'+topTitle
            bottomTitle = '正常' if not bottomTitle else '副题错误：'+bottomTitle

            if (title=='正常' and content=='正常' and source=='正常' and author=='正常'
               and _time=='正常' and topTitle=='正常' and bottomTitle=='正常'):
                EVALUTE = '正常'
            else:
                EVALUTE = '错误'

            total_field = [SCRIPT_NAME, IR_SITENAME, CHANNAL_PATH, DOCCHANNEL, 
                          SITE_URL, START_TIME,USE_TIME, index, title, content, source,
                          author, _time, topTitle, bottomTitle, EVALUTE]
            output_line = '^'.join(total_field) + '\n'

        # for total result
        if spider.test:
            print('\n\n\n\nINFO >>>>>>>>>>>>>>>:',output_line)
        else:
            with open(self.get_filename(),'a',encoding=RESULT_ENCODING) as f:
                f.write(output_line)

        # for wrong result 
        if EVALUTE != '正常':
            wrong_total_field =  [IR_SITENAME, CHANNAL_PATH, DOCCHANNEL, 
                                SITE_URL, index, title, content, source,
                                author, _time, topTitle, bottomTitle]
            wrong_output_line = '^'.join(wrong_total_field) + '\n'
            if spider.test:
                print('WRONG >>>>>>>>>>>>>>>>>>:',wrong_output_line,'\n\n\n\n')
            else:
                f = open(self.get_wrong_filename(),encoding=RESULT_ENCODING)
                all_line = f.readlines()
                f.close()
                if wrong_output_line not in all_line:
                    with open(self.get_wrong_filename(),'a',encoding=RESULT_ENCODING) as f:
                        f.write(wrong_output_line)

        # if script run success ,remove its name from uncheck_list
        if not spider.test:
            self.remove_success_from_uncheck_file(SITE_URL)

