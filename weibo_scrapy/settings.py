# -*- coding: utf-8 -*-

BOT_NAME = 'weibo_scrapy'

SPIDER_MODULES = ['weibo_scrapy.spiders']

NEWSPIDER_MODULE = 'weibo_scrapy.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 0.1

# COOKIES_ENABLED = True

TELNETCONSOLE_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "s.weibo.com",
    "Pragma": "no-cache",
    "Referer": "https://s.weibo.com/weibo?q=%E7%BF%9F%E5%A4%A9%E4%B8%B4&typeall=1&suball=1&timescope=custom:2019-02-01-0:2019-02-01-1&Refer=g",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
}

SPIDER_MIDDLEWARES = {
   'weibo_scrapy.middlewares.WeiboScrapySpiderMiddleware': 543,
}

DOWNLOADER_MIDDLEWARES = {
   'weibo_scrapy.middlewares.WeiboScrapyDownloaderMiddleware': 543,
}

LOG_LEVEL = 'DEBUG'

# LOG_FILE = "log"

ITEM_PIPELINES = {
    'weibo_scrapy.pipelines.WeiboExcelPipeline': 300,
    'weibo_scrapy.pipelines.WeiboDbPipeline': 200
}


WEIBO_Q = "翟天临"

START_TIME = "2019-02-1-0"

END_TIME = "2019-03-1-0"

COOKIES = "_s_tentry=-; Apache=3612868906783.687.1557660938879; SINAGLOBAL=3612868906783.687.1557660938879; WBStorage=dbba46d4b213c3a3|undefined; ULV=1557660939092:1:1:1:3612868906783.687.1557660938879:; WBtopGlobal_register_version=5c10f3128cf400c5; SCF=AiwUachNkoa6KheXshL7GYDE_nK3UBBZiKeN7Le2thxddObfLS9Xdl8sWZIAW_eUbpl5vtLxXHLl9EqOCb6hpgA.; SUB=_2A25x3HVhDeRhGeNG6VUU8ivPzDqIHXVSqOGprDV8PUNbmtBeLVj9kW9NS3jWP3mKUOkmBOa17cAPPDgRv-IXRnPv; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWUw9pj1lV--F9.qjJloMQE5JpX5K2hUgL.Fo-ReoMfeo-0S0q2dJLoI0qLxKBLB.eL1-2LxKBLBonL122LxK-LBKBLBK.LxKML1-2L1hBLxKqLBo-LBoMLxKMLB.zLBo-t; SUHB=0auAia03woUY1o; ALF=1558265781; SSOLoginState=1557660977; un=15170307370"

# mysql配置
MYSQL_SETTING = {
    "user": "",
    "password": "",
    "host": "",
    "db": "",
}