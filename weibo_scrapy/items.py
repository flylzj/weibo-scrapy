# -*- coding: utf-8 -*-
import scrapy

class WeiboUserInfoItem(scrapy.Item):
    # 用户id
    weibo_user_id = scrapy.Field()
    # 昵称
    weibo_username = scrapy.Field()
    # 性别
    weibo_sexual = scrapy.Field()
    # 所在地
    weibo_location = scrapy.Field()
    # 生日
    weibo_birth = scrapy.Field()
    # 个人简介
    weibo_desc = scrapy.Field()
    # 注册时间
    weibo_sign_up_date = scrapy.Field()



class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    weibo_mid = scrapy.Field()
    weibo_user_id = scrapy.Field()
    weibo_username = scrapy.Field()
    weibo_content = scrapy.Field()
    weibo_pub_time = scrapy.Field()
    weibo_post_count = scrapy.Field()
    weibo_comment_count = scrapy.Field()
    weibo_like_count = scrapy.Field()
    # 如果是转发微博，转发的来源
    weibo_from_url = scrapy.Field()

    start_time = scrapy.Field()
    end_time = scrapy.Field()
    user_info = scrapy.Field()

