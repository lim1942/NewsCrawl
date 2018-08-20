
一.依赖

	python 3.6
	frame: scrapy 1.5  +  scrpyd
	系统: windows


二.监控原理

    监控主要的原理是通过脚本验证网页中包裹字段的标签是否存在，来判断网页结构是否发生变化，进而达到
    监控的目的。
  	通过为每个采集点写一个爬虫脚本，用脚本去解析采集点的首页和细缆页达到监控的目的。首页解析其包含
  	的细缆链接（看首页是不是能正常访问，能不能取到细缆页的链接，只要不能就判断首页错误），细缆页解
  	析每篇新闻所需的特定字段（如果某个字段的标签不能取到就说明该细缆页的该字段的网页结构发生改变）。 
  	监控的解析的方式有xpath路径，css样式，正则表达式。把所有采集点的监控情况输出到当天的汇总日志，
  	再把汇总检查日志的错误采集点收集到当天的错误日志中。


三.监控流程

	1、开始：通过脚本或者接口的方式启动监控程序。
	2、获取待运行所有脚本：获取监控程序中的所有监控脚本的一个数组，数组中的脚本按照字母顺序排序。
	3、获取一个脚本执行：按照顺序获取一个监控脚本进行执行。
	4、概览页监控：使用脚本中的xpath（标签的路径定位）、css（标签的样式定位）或书写正则表达式 去匹
	 配概览页，看概览页是否正常。监控中能出现的情况有：正常，细缆页无法访问，细缆页结构改变）
	5、对概览页的监控情况进行判断：不正常（结构改变，网络异常无法访问），导致后面的细缆检查无法
	 进行，直接输出错误到检查日志，输出的内容为概览页异常，细缆页未检查。获取下一个监控脚本执行。
	 正常：进行后面的流程
	6、获取所有细缆页的链接：在概览页正常的情况下，获取到了所有细缆页的链接。
	7、加载细缆页并进行监控：监控最多不超过20个细缆页。使用xpath、css或正则去匹配细缆页中包裹
	（标题，时间，来源，作者，正文，引题，副题）字段的标签。监控中能出现的情况有：正常，细缆页
	 无法加载访问，细缆页结构改变）
	8、监控结果输出到日志文件：把针对这个采集点的监控情况输出到日志。进行下一个脚本。

	注：针对多模板的网页，采用采集多个特定点【例：author、author1...在判断是利用or只要一项成立即可判
	断为原网页未变化（存在一定误报）】。对于外链链接直接在采集过程中排除即可。对于无法用xpath定位的数据
	，例如网页源码中用js加载的数据，可采用正则的方式定位所要监控内容的位置。



三.目录结构

	NewsCrawl：为项目的根目录
	NewsCrawl\disable_script_list.txt: 该文件为配置错误的脚本目录，通过这个文件可以查看那些监控脚本书写错误。
	NewsCrawl\NewsCrawl\: 为项目的代码所在目录，代码内容包括每个采集点的监控脚本，日志格式控制，
		日志显示字段的提取规则，项目的整体设置，每个脚本的个性化设置，监控过程中的一些中间键设置。
	NewsCrawl\result\：项目的日志目录，按日期来给日志命名，日志记录了采集点的监控情况
	NewsCrawl\result\wrong\: 为程序对采集点检查的错误日志目录，此日志中出现的采集点均为结构发生改动的采集点。
	NewsCrawl\logs\：为程序的运行日志，显示程序运行过程的错误，和脚本书写相关的错误
	NewsCrawl\work\ ：放excel的目录，有两种excel。  gen_spiders_from_excel用来生成脚本模板的excel，
		start_check_from_excel 需要进行监控采集点汇总的excel
	NewsCrawl\gen_spider.py : 用NewsCrawl\work\ 里的excel自动生成模板（需要再配置即可运行）
	NewsCrawl\scrapyd_server.bat : 启动scrapyd服务，该服务确保了程序的调度运行。
	NewsCrawl\scrapyd_task.py : scrapyd任务相关类，实现了推任务脚本到scrapyd，进行任务调度，查看任务的执行状况。
	NewsCrawl\start.py ： 执行excel清单中的待检查的采集点脚本，开始检查。
	NewsCrawl\watch.py : 查看脚本的执行状况
	其它目录和文件：为项目自带，不可删除，与程序的逻辑无关。



四.使用方法

  监控脚本配置：
   1.把待生成脚本的excel清单放入NewsCrawl\work\start_check_from_excel\ 目中的
    （注意格式，按照该目录中的excel例子一样）。
   2.python 运行 gen_spider.py即可批量生成脚本。生成的脚本是需要再配置的。
   3.配置脚本中链接提取规则，字段的提取规则，完成配置的脚本再下次检查中就会运行

  运行检查：
   1.先把要检查采集点清单的excel放入 NewsCrawl\work\start_check_from_excel\ 目录中
    （注意格式，按照该目录中的excel例子一样）
   2.先点击运行scrapyd_server.bat，启动scrapyd服务，不要关闭服务的窗口。
   3.使用python 运行 start.py 按照NewsCrawl\work\start_check_from_excel\ 目录
     中excel的清单 调度爬虫程序的运行，运行清单中的所有脚本。
   4.python 运行 watch.py 查看scrapyd中脚本的执行状况，全部脚本运行结束了再检查监控结果。
   5.监控结束，查看NewsCrawl\result\ 里的日志查看运行脚本采集点的监控状态。
   6.查看NewsCrawl\disable_script_list.txt 文件有哪些脚本没有运行，对照NewsCrawl\logs\
     里的程序运行日志把脚本修改正确。



五.监控脚本书写规范

   提取字段的xpath或者css的规则写的越详细越好，这样原网站一稍稍变动，检测就能报错，起到更好的检测作用
	1.类继承 CrawlSpider
	  xxxClass(CrawlSpider)
	2.类属性
	  IR_SITENAME：采集点网站名
      CHANNAL_PATH：采集点栏目名
      DOCCHANNEL：采集点栏目别名
	  name:采集点的名字
	  start_urls: 开始爬虫的url列表
	  rules : 从首页中提取橄榄页的链接，参数灵活，有多种提取方式，xptah，正则，css，链接排除....	
	3.类方法
	  parse_start_url:从首页检查url提取是否正常，并return提取的内容
	  parse_item:从细缆页从提取具体的字段，并return提取的结果