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

COOKIES = ""

# mysql配置
MYSQL_SETTING = {
    "user": "",
    "password": "",
    "host": "",
    "db": "",
}