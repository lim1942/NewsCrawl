# -*- coding: utf-8 -*-
# @Author: xb12369
# @Date:   2018-08-14 11:26:48
# @Last Modified by:   xb12369
# @Last Modified time: 2018-08-14 11:39:03
from scrapyd_task import my_scrapyd

if __name__ == '__main__':
	obj = my_scrapyd()
	obj.spiders_deploy_to_scrapyd()
	obj.run_spiders_from_excel()