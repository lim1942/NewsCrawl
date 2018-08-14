# -*- coding: utf-8 -*-
# @Author: lim
# @Date:   2018-08-13 13:52:04
# @Last Modified by:   xb12369
# @Last Modified time: 2018-08-14 11:30:35

import os
import xlrd
import time
import json
import requests

from tools import excel_ensure


UNCHECK_FILE_ENCODING = 'utf-8'
UNCHECK_PATH = 'disable_script_list.txt'
EXCEL_PATH = 'work/start_check_from_excel/'


class my_scrapyd:


    def __init__(self):
        self.base_url = 'http://localhost:6800/'


    def spiders_deploy_to_scrapyd(self):
        os.system('scrapyd-deploy')
        print('Finish deploy spider to scrapyd !!! \n\n\n')


    def download(self,url,data=None):
        try:
            if not data:
                r = requests.get(url,timeout=5) 
            else:
                r = requests.post(url,data,timeout=5)
            if r.status_code == 200:
                data = json.loads(r.text)
                if data['status'] == 'ok':
                    return data
                else:
                    print(data,'\n')
                    raise  Exception('data error')
            else:
                raise Exception('status_code error')
        except Exception  as e:
            print(e,'-----',url,'   data=',data)


    def get_node_status(self):
        url = self.base_url +'daemonstatus.json'
        data = self.download(url)
        if data:
            return data
        else:
            print('get_index error')


    def get_projects(self):
        url = self.base_url +'listprojects.json'
        data = self.download(url)
        if data:
            projects = data['projects']
            projects.remove('default')
            return projects
        else:
            print('get_projects error')


    def get_spiders(self,projectname):
        url = self.base_url +'listspiders.json?project=' + projectname
        data = self.download(url)
        if data:
            spiders = data['spiders']
            return {'projectname':projectname,'spiders':spiders}
        else:
            print('get_spiders error')


    def run_spider(self,projectname,spider):
        url = self.base_url +'schedule.json'
        url_data = {'project':projectname,'spider':spider}
        data = self.download(url,url_data)
        if data:
            jobid = data['jobid'] 
            print('Sucessful push  {}   >>   {}'.format(spider,jobid))
            return jobid
        else:
            print('run_spider error')


    def run_spiders(self,dict_spiders):
        success = []
        failed = []
        projectname = dict_spiders['projectname']
        spiders = dict_spiders['spiders']
        for spider in spiders:
            jobid = self.run_spider(projectname,spider)
            if jobid:
                success.append({'projectname':projectname,'spider':spider,'job':jobid})
            else:
                failed.append({'spider':spider,'projectname':projectname})
        return {'success':success,'failed':failed}


    def kill_spider(self,projectname,jobid):
        url = self.base_url +'cancel.json'
        url_data = {'project':projectname,'job':jobid}
        data = self.download(url,url_data)
        if data:
            prevstate = data['prevstate']
            return prevstate
        else:
            print('kill_spider error')


    def get_jobs_status(self,projectname):
        url = self.base_url +'listjobs.json?project=' + projectname
        data = self.download(url)
        jobs_status = dict()
        if data :
            jobs_status['pending'] = data['pending']
            jobs_status['running'] = data['running']
            jobs_status['finished'] = data['finished']
            return jobs_status
        else:
            print('get_jobs_status error')


    def one_project_auto_start(self):

        projectname = 'NewsCrawl'
        print('get a project <',projectname,'>')

        dict_spiders = self.get_spiders(projectname)
        if not dict_spiders:
            print('get spider error')
            return

        spiders = dict_spiders['spiders']
        spiders_len = len(spiders)

        print('Success get {} spiders from < {} >'.format(spiders_len,projectname))
        print(spiders)
        print('process will push all spiders now ...\n')

        push_status = self.run_spiders(dict_spiders)
        print(push_status,'\n')
        return push_status


    def one_project_stauts(self):
        projectname = 'NewsCrawl'
        status = self.get_jobs_status(projectname)
        if not status:
            print('get status error')
            return
        print(status,'\n')
        return status


    def write_spider_to_uncheck_file(self,filename,line):
        con = ''
        if os.path.exists(filename):
            f = open(filename,encoding=UNCHECK_FILE_ENCODING)
            con = f.readlines()
            f.close()
        if line not in con:
            with open(filename,'a',encoding=UNCHECK_FILE_ENCODING) as f:
                f.write(line)


    def run_spiders_from_excel(self): 
        projectname = 'NewsCrawl'  
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

        excel_filename = excel_ensure(get_excel_filename())
        if not excel_filename:
            return

        r_file = xlrd.open_workbook(excel_filename)
        try:
            table = r_file.sheet_by_index(0)
        except Exception as e:
            print(e)

        if table.ncols != 5:
            print('Bad excel format, please check it out !!!  change it into 5 cols')
            return

        spiders = []
        for i in range(table.nrows):
            row  = table.row_values(i)
            if (('网站名' in row) and ('栏目名' in row)) or (('Column1' in row) and ('Column2' in row)):
                continue
            spider = row[0]
            res = self.run_spider(projectname,spider)
            sitename = row[1]
            channel_path = row[2]
            docchannel = row[3]
            weburl = row[4]
            line = '^'.join([time.strftime('%Y-%m-%d'),spider,sitename,channel_path,docchannel,weburl,'未检查']) + '\n'
            self.write_spider_to_uncheck_file(UNCHECK_PATH, line)





# if __name__ == '__main__':
#     o = my_scrapyd()
#     o.spiders_deploy_to_scrapyd()
#     o.run_spiders_from_excel()
    # o.one_project_auto_start()
    # o.one_project_stauts()
