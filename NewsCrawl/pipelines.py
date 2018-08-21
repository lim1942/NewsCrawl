# -*- coding: utf-8 -*-
# @Author: lim
# @Date:   2018-08-13 13:52:04
# @Last Modified by:   xb12369
# @Last Modified time: 2018-08-21 09:01:49

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import time

OUTPUT_ENCODING = 'utf-8'



class NewscrawlPipeline(object):

    def __init__(self):  
        # a list to collect spider`s items
        self.result = []   


    def get_filename(self):
        """get a file name for wirte output_line"""
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'result')
        if not os.path.exists(path):
            os.mkdir(path)
        filename = os.path.join(path,self.get_date_name())
        return filename


    def get_wrong_filename(self):
        """get a file name for wirte wrong output_line"""
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'result')
        wrong_path = os.path.join(path,'wrong')
        if not os.path.exists(wrong_path):
            os.mkdir(wrong_path)
        wrong_filename = os.path.join(wrong_path,self.get_date_name())
        return wrong_filename


    def get_date_name(self):
        """return datetime filename"""
        return time.strftime('%Y-%m-%d') + '.txt'


    def remove_success_spider_name_from_disable_script_list_file(self,SCRIPT_NAME):
        """if this spider run successful and parse fields correct, 
           remove its name from disable_script_list.txt"""

        DISABLE_SCRIPT_FILE_ENCODING = 'utf-8'

        disable_script_list_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        disable_script_list_file_filename = os.path.join(disable_script_list_file_path,'disable_script_list.txt')
        with open(disable_script_list_file_filename,encoding=DISABLE_SCRIPT_FILE_ENCODING) as f:
            content = f.readlines()
        with open(disable_script_list_file_filename,'w+',encoding=DISABLE_SCRIPT_FILE_ENCODING) as f:
            filter_con = ''
            for line in content:
                if SCRIPT_NAME not in line:
                    filter_con += line
            f.write(filter_con)



    def process_item(self, item, spider):
        """Gather one spider`s items to a list"""
        self.result.append(item)
        return item


    def open_spider(self, spider):
        """As spider start ,open two file(one for
         output_line another for wrong output_line)
         and write header into them"""

        # record time when spider start
        self.start = time.time()
        self.start_date = time.strftime('%H:%M:%S')

        # write output_line file header
        filename = self.get_filename()
        field_head = ('脚本名^网站名^栏目名^栏目别名^网址^开始时间^用时^首页检擦^标题^正文^来源^作者^时间^引题^副题^采集点评估\n')
        if not os.path.exists(filename):
            with open(filename,'w', encoding=OUTPUT_ENCODING) as f:
                f.write(field_head)

        # write wrong output_line file header
        wrong_filename = self.get_wrong_filename()
        wrong_field_head = ('网站名^栏目名^栏目别名^网址^首页检擦^标题^正文^来源^作者^时间^引题^副题\n')
        if not os.path.exists(wrong_filename):
            with open(wrong_filename,'w', encoding=OUTPUT_ENCODING) as f:
                f.write(wrong_field_head)



    def close_spider(self, spider):

        """as spide close,pick fields and processing them to file """

        # record a time when spider close
        self.end = time.time()

        # pick sixteen fields from a spider ======
        SCRIPT_NAME = spider.name
        IR_SITENAME = spider.IR_SITENAME
        CHANNAL_PATH = spider.CHANNAL_PATH
        DOCCHANNEL = spider.DOCCHANNEL
        SITE_URL = spider.start_urls[0]                # start url
        START_TIME = self.start_date                   # spider start date 
        USE_TIME = str(self.end-self.start)[:4]+'s'    # spider use time
        index = '' 
        title = ''
        content = ''
        source = ''
        author = ''
        _time = ''
        topTitle = ''
        bottomTitle = ''
        EVALUTE = ''                                   # field to Evalute this collection poiont


        # Pick condition 1:  >>>> just crawl index or  crawl nothing
        if len(self.result)<=1:
            if len(self.result) == 0:
                EVALUTE = '概览页无响应' 
            else:
                indexLen = self.result[0].get('indexLen')
                index = '错误' if indexLen is None else '正常'
                EVALUTE ='细缆页无响应'

        # Pick condition 2: >> crawl all page successfull 
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


        # processing all fields to a output_line
        # A line contain all Status of the colloction point`s situation
        total_field = [SCRIPT_NAME, IR_SITENAME, CHANNAL_PATH, DOCCHANNEL, 
                      SITE_URL, START_TIME,USE_TIME, index, title, content, source,
                      author, _time, topTitle, bottomTitle, EVALUTE]
        output_line = '^'.join(total_field) + '\n'


        # export output_line to file (except test mode)
        if spider.test:
            print('\n\n\n\nINFO >>>>>>>>>>>>>>>:',output_line)
        else:
            with open(self.get_filename(),'a',encoding=OUTPUT_ENCODING) as f:
                f.write(output_line)


        # Export wrong output_line to file (except test mode) 
        if EVALUTE != '正常':
            wrong_total_field =  [IR_SITENAME, CHANNAL_PATH, DOCCHANNEL, 
                                SITE_URL, index, title, content, source,
                                author, _time, topTitle, bottomTitle]
            wrong_output_line = '^'.join(wrong_total_field) + '\n'
            if spider.test:
                print('WRONG >>>>>>>>>>>>>>>>>>:',wrong_output_line,'\n\n\n\n')
            else:
                with open(self.get_wrong_filename(),'r+',encoding=OUTPUT_ENCODING) as f:
                    if wrong_output_line not in f.read():
                        f.write(wrong_output_line)


        # As a spider start ,wiil add it`s name to disable_script_list.txt (except test mode)
        # if script run and parse-fields successful ,remove its name from disable_script_list.txt that means this script is correct  (except test mode)
        if (not spider.test) and output_line:
            self.remove_success_spider_name_from_disable_script_list_file(SCRIPT_NAME)

