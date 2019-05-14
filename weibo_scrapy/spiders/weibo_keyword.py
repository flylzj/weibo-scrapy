# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import WeiboItem, WeiboUserInfoItem
from ..util import create_date
import datetime
import os
import re


class WeiboKeywordSpider(scrapy.Spider):
    cookies = None
    name = 'weibo_keyword'
    search_weibo_base_url = "https://s.weibo.com/weibo?q={}&typeall=1&suball=1&timescope=custom:{}:{}&Refer=g"
    user_info_base_url = "https://weibo.com/p/100505{}/info?mod=pedit_more"
    host = "https://s.weibo.com"
    info_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        "Host": "weibo.com",
    }
    cookies_dict = None


    # 用来把cookie字符串解析成字典
    @staticmethod
    def parse_cookies(cookies_str):
        cookies = [cookie.strip() for cookie in cookies_str.split(";")]
        cookies_dict = dict()
        for cookie in cookies:
            k = cookie.split("=")[0]
            v = cookie.split("=")[1]
            cookies_dict[k] = v
        return cookies_dict

    # 爬虫的入口函数
    def start_requests(self):
        '''
        这里说一下为什么要分时间段爬取，因为搜索结果只能返回50页的数据，如果不分时间段我们只能拿到50页数据
        :return:
        '''
        # 从设置总获取关键词
        q = self.settings.get('WEIBO_Q', 'python')
        # 从设置中获取时间段
        data_list = create_date(
            self.settings.get('START_TIME', (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d-%H')),
            self.settings.get('END_TIME', datetime.datetime.today().strftime('%Y-%m-%d-%H'))
        )
        # 从设置中获取cookies
        self.cookies = self.settings.get('COOKIES')
        # 遍历时间段
        for i in range(len(data_list) - 1):
            page = 1
            start_time = data_list[i]
            end_time = data_list[i + 1]
            # 构造url
            start_url = self.search_weibo_base_url.format(q, start_time, end_time)
            meta = {
                "page": page,
                "count": 0,
                "start_time": start_time,
                "end_time": end_time,
                "url_list": [start_url]  # 这里放一个url list， 用来过滤爬过的url，因为虽然到了最后一页，他还是会有下一页这个标签
            }
            self.cookies_dict = self.parse_cookies(self.cookies)
            # 返回请求给parse_weibo函数解析
            yield scrapy.Request(start_url, meta=meta, callback=self.parse_weibo, cookies=self.cookies_dict)

     # 解析响应的请求, 用的是BeautifulSoup
    def parse_weibo(self, response):
        meta = response.meta
        soup = BeautifulSoup(response.text, "lxml")
        # 找到所有微博的div标签
        weibos = soup.find_all("div", attrs={"action-type": "feed_list_item"})

        # 遍历微博并提取信息
        for weibo in weibos:
            weibo_item = WeiboItem()
            weibo_user_info_item = WeiboUserInfoItem()
            weibo_item['user_info'] = weibo_user_info_item
            # mid
            weibo_item['weibo_mid'] = weibo.get('mid')

            user_info = weibo.find('a', attrs={"class": "name", "nick-name": re.compile(r'.+')})
            # 用户id
            weibo_item['weibo_user_id'] = \
                re.search(
                    r'//weibo.com/(\d+).*',
                    user_info.get('href') if user_info.get('href') else "//weibo.com/0000000000?refer_flag=1001030103_"
                ).groups()[0]
            # 用户昵称
            weibo_item['weibo_username'] = user_info.text.strip()
            weibo_user_info_item['weibo_user_id'] = weibo_item['weibo_user_id']
            weibo_user_info_item['weibo_username'] = weibo_item['weibo_username']


            weibo_info = weibo.find("p", attrs={"node-type": "feed_list_content_full", "nick-name": re.compile(r'.+')})
            if not weibo_info:
                # 说明文章很短，不需要展开全文
                weibo_info = weibo.find("p",
                                        attrs={"node-type": "feed_list_content", "nick-name": re.compile(r'.+')})
            # 微博原文
            weibo_item['weibo_content'] = weibo_info.text.strip().strip('收起全文d')

            weibo_pub = weibo.find_all('p', attrs={'class': 'from'})[-1].a.text
            # 发布时间
            weibo_item['weibo_pub_time'] = weibo_pub.strip()

            weibo_subinfo = weibo.find('div', attrs={"class": "card-act"}).find_all('li')
            # 转发数量
            weibo_item['weibo_post_count'] = weibo_subinfo[1].text.strip().strip("转发")
            weibo_item['weibo_post_count'] = int(weibo_item['weibo_post_count'])\
                if weibo_item['weibo_post_count'] else 0

            # 评论数量
            weibo_item['weibo_comment_count'] = weibo_subinfo[2].text.strip().strip("评论")
            weibo_item['weibo_comment_count'] = int(weibo_item['weibo_comment_count'])\
                if weibo_item['weibo_comment_count'] else 0

            # 点赞数量
            weibo_item['weibo_like_count'] = weibo_subinfo[3].text.strip()
            weibo_item['weibo_like_count'] = int(weibo_item['weibo_like_count'])\
                if weibo_item['weibo_like_count'] else 0

            # 转发微博
            weibo_from_info = weibo.find('div', attrs={"class": "card-comment"})
            if not weibo_from_info:
                weibo_item['weibo_from_url'] = ""
            else:
                weibo_item['weibo_from_url'] = self.host + weibo_from_info.find('p', attrs={"class": "from"}).a.get('href')[1:]
            weibo_item['start_time'] = meta.get('start_time')
            weibo_item['end_time'] = meta.get('end_time')
            # self.logger.info(weibo_item)
            meta["count"] += 1
            meta['item'] = weibo_item
            # 提取完微博信息之后要构造用户信息url用来提取用户信息
            yield scrapy.Request(
                self.user_info_base_url.format(weibo_item['weibo_user_id']),
                meta=meta,
                callback=self.parse_user_info,
                dont_filter=True,
                cookies=self.cookies_dict,
                headers=self.info_headers,
            )
        try:
            # 这里是分页判断，先找有没有下一页标签
            page_info = soup.find('div', attrs={"class": "m-page"}).find('a', attrs={"class": "next"})
            next_url = self.host + page_info.get('href')
        except Exception as e:
            next_url = None

        # 如果有下一页标签并且下一页我们没有爬过就爬下一页，因为最后一页的下一页可能是第一页，所以做了这个判断
        if next_url and next_url not in meta.get('url_list'):
            meta['page'] += 1
            self.logger.info('next_page: {}'.format(next_url))
            # 把爬过的url记录在url_list里
            meta['url_list'].append(next_url)
            yield scrapy.Request(next_url, meta=meta, callback=self.parse_weibo)

    # 解析用户信息
    def parse_user_info(self, response):
        meta = response.meta
        weibo_item = meta['item']
        soup = BeautifulSoup(response.text, 'lxml')
        scripts = soup.find_all('script')
        html = ""
        # 用户信息都在通过js加载的，所以需要用正在提取
        for script in scripts:
            res = re.search(r'"html":"([\S\s]+)"}\)', script.text)
            if res:
                html += res.groups()[0]
        # 写好信息提取的正则
        infos = re.findall(r'<li class=\\"li_1 clearfix\\">[\s\S]*?<span class=\\"pt_title S_txt2\\">(.*?)<\\/span>[\s\S]*?<span class=\\"pt_detail\\">([\S\s]*?)<\\/span>[\s\S]*?<\\/li>', html)
        # 过滤出我们想要的信息
        for info in infos:
            if info[0] == '性别：':
                weibo_item['user_info']['weibo_sexual'] = info[1]
            elif info[0] == '所在地：':
                weibo_item['user_info']['weibo_location'] = info[1]
            elif info[0] == "生日：":
                weibo_item['user_info']['weibo_birth'] = info[1]
            elif info[0] == "简介：":
                weibo_item['user_info']['weibo_desc'] = info[1]
            elif info[0] == '注册时间：':
                weibo_item['user_info']['weibo_sign_up_date'] = info[1].strip('\\r\\n').strip()
            else:
                pass
        # 把拿到的数据传到pipeline进行入库
        yield weibo_item