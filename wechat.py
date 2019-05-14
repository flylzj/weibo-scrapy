# coding: utf-8
import requests
from bs4 import BeautifulSoup
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import WechatArticle, Base
from datetime import datetime
import time
import openpyxl


class WechatSogou(object):
    def __init__(self):
        self.search_api = 'https://weixin.sogou.com/weixin'
        self.host = "https://weixin.sogou.com"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Host": "weixin.sogou.com",
            "Pragma": "no-cache",
            "Cookie": "IPLOC=CN3601; SUID=DAC7496F8D6B900A000000005CB3E71E; SUV=0009EAD1DA4016805CC50C6C85194112; CXID=F0D55330555D8679F3225E890CD26F5F; ad=pLlmSlllll2thVGjlllllV8wUZUlllllb1Xp3kllllwlllll4A7ll5@@@@@@@@@@; ABTEST=7|1557733169|v1; JSESSIONID=aaagQB0H4_Jgb8AcIOzPw; PHPSESSID=9p6d675bp1lud5ls1o155hk342; weixinIndexVisited=1; ppinf=5|1557752745|1558962345|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo4OmZseXRoaWVmfGNydDoxMDoxNTU3NzUyNzQ1fHJlZm5pY2s6ODpmbHl0aGllZnx1c2VyaWQ6NDQ6bzl0Mmx1RzVuWXotNWpBQ1VYekFma1ZMSkVnWUB3ZWl4aW4uc29odS5jb218; pprdig=QOmAdJ9lBSC2cof9AlREXO2jXec9A9j9VL3n9JmbhXx8t3kSe8SIfyRILZRKsvJSGQlMAXV-05YI3-sVAsZ7y9r_-SNVx5yVTRXlQGLeHM9MOUlZ760TOe5gyQprPcWIPvgIogLJoYuwiwdm8i6oKDtcnG5eThCzWSNN5JmWcPE; sgid=20-40627857-AVzZa6mrSrkQe1uqKnpP0lA; ppmdig=155775274500000094421377fba74850cf2299b7e5322d41; sct=1; seccodeErrorCount=2|Mon, 13 May 2019 13:43:37 GMT; SNUID=BA5BD5F39D99145997A55B539DED088B; seccodeRight=success; successCount=1|Mon, 13 May 2019 13:44:11 GMT; refresh=1",
            "Referer": "https://weixin.sogou.com/antispider/?from=%2fweixin%3Ftype%3d2%26s_from%3dinput%26query%3d%27%E9%9D%9E%E9%81%97%E8%BF%9B%E7%A4%BE%E5%8C%BA%27%26ie%3dutf8%26_sug_%3dn%26_sug_type_%3d%26page%3d44",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
        }
        self.wechat_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
        }
        self.session = requests.session()

    def search_article(self, keyword, page=1):
        params = {
            "type": 2,
            "s_from": "input",
            "query": keyword,
            "ie": "utf8",
            "_sug_": "n",
            "_sug_type_": "",
            "page": page
        }
        try:
            r = self.session.get(self.search_api, params=params, headers=self.headers)
            r.encoding = r.apparent_encoding
            print(r.url)
            if 'antispider' in r.url:
                self.code_mode(r.url)
                r = self.session.get(self.search_api, params=params, headers=self.headers)
                r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, 'lxml')
            articles = soup.find_all('li', attrs={'id': re.compile(r'sogou_vr_11002601_box_\d*')})
            for article in articles:
                href = article.find('a', attrs={'uigs': re.compile(r'article_title_\d')})
                if href:
                    href = href.get('data-share')
                    article_url = self.get_article_url(href)
                    yield self.get_article_detail(article_url)
                else:
                    print('no href', article)
        except Exception as e:
            print(e)
            return None

    def code_mode(self, url):
        print('需要验证码')
        print("请访问 {} 并输入验证码".format(url))
        print("输入完成后请输入cookies")
        cookies = input("输入cookies>")
        self.headers.update({'Cookie': cookies})

    def get_code(self, code_url):
        try:
            r = self.session.get(code_url, headers=self.headers)
            soup = BeautifulSoup(r.text, 'lxml')
            img_path = soup.find('img', attrs={'id': 'seccodeImage'}).get('src')
            with open('code.jpg', 'ab') as f:
                root_path = "https://weixin.sogou.com/antispider/"
                r = self.session.get(root_path + img_path, headers=self.headers)
                f.write(r.content)
        except Exception as e:
            print(e)

    def get_article_url(self, sogou_url):
        try:
            r = self.session.get(sogou_url, headers=self.headers)
            r.encoding = r.apparent_encoding
            return r.url
        except Exception as e:
            print(e)
            return None

    def get_article_detail(self, article_url):
        try:
            r = requests.get(article_url, headers=self.wechat_headers)
            soup = BeautifulSoup(r.text, 'lxml')
            nickname = soup.find('strong', attrs={'class': 'profile_nickname'}).text
            wechat_id = soup.find('span', attrs={'class': 'profile_meta_value'}).text
            title = soup.find('h2', attrs={'class': 'rich_media_title', 'id': 'activity-name'}).text.strip()
            content = soup.find('div', attrs={'id': 'js_content'})
            if content:
                content = content.text
                content = re.sub(r'\s', '', content)
                content = content.strip()
            date = re.search(r'ct="(\d{10})"[\S\s]*publish_time = "(.*?)" \|\|', r.text).groups()
            return {
                "nickname": nickname,
                "wechat_id": wechat_id,
                "title": title,
                "content": content,
                "date": date,
                "url": r.url
            }
        except Exception as e:
            print(e)
            return None

    def crawl(self, keyword, total_page, time_interval=3):
        for i in range(1, total_page + 1):
            for article in self.search_article(keyword, i):
                yield article
            print('sleep 3 second')
            time.sleep(time_interval)


class WechatDb(object):
    def __init__(self):
        self.engine = create_engine('sqlite:///./data.db')
        self.Session = sessionmaker(bind=self.engine)
        self.init_table()

    def init_table(self):
        Base.metadata.create_all(self.engine)

    def clear_table(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    @staticmethod
    def convert_date(s):
        try:
            return datetime.strptime(s, '%Y-%m-%d').date()
        except Exception as e:
            return datetime.today().date()

    # 导出为excel函数
    def output_excel(self):
        try:
            session = self.Session()
            articles = session.query(WechatArticle).all()
            wb = openpyxl.Workbook()
            sheet = wb.active
            title = [
                "公众号名称",
                "微信号",
                "文章标题",
                "文章内容",
                "发布日期",
                "链接",
                "t" # 这一列是为了让excel更美观一点
            ]
            sheet.append(title)
            for article in articles:
                sheet.append([
                    article.nickname,
                    article.wechat_id,
                    article.title,
                    article.content,
                    article.pub_date.strftime('%Y-%m-%d'),
                    article.url,
                    "t"
                ])
            wb.save('data.xlsx')
        except Exception as e:
            print(e)

    def add_article(self, data):
        try:
            session = self.Session()
            article = WechatArticle(
                nickname=data.get('nickname'),
                wechat_id=data.get('wechat_id'),
                title=data.get('title'),
                content=data.get('content'),
                pub_date=self.convert_date(data.get('date')[1]),
                pub_ct=int(data.get('date')[0]),
                url=data.get('url')
            )
            session.add(article)
            session.commit()
            print('add {} success'.format(data.get('title')))
        except Exception as e:
            print(e)




if __name__ == '__main__':
    ws = WechatSogou()
    wd = WechatDb()
    # wd.clear_table()

    # 每次时间间隔
    time_interval = 3
    keyword = "非遗进社区"
    for article in ws.crawl(keyword, 100, time_interval):
        wd.add_article(article)
    # 导出excel
    wd.output_excel()