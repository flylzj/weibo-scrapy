# 基于[微博搜索](https://s.weibo.com)的关键词微博和用户信息爬取

## 项目依赖

* scrapy
* openpyxl
* sqlalchemy
* BeautifulSoup

### 运行前的准备

* 在settings.py中修改WEIBO_Q(这个变量是要搜索的关键词)

* 配置START_TIME和END_TIME,这两个分别是筛选的开始时间和结束时间

* 从浏览器复制cookies给COOKIES变量

* 配置MYSQL_SETTING

### 运行

`scrapy crawl weibo_keywrod` 或 python run.py