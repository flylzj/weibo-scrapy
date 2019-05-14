# coding: utf-8
import datetime


def create_date(date_start, date_end):  # 创建日期列表
    date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d-%H')
    date_end = datetime.datetime.strptime(date_end, '%Y-%m-%d-%H')
    date_list = []
    date_list.append(date_start.strftime('%Y-%m-%d') + "-" +str(date_start.hour))
    while date_start < date_end:  # 日期叠加一天
        date_start += datetime.timedelta(hours=+1)
        date_list.append(date_start.strftime('%Y-%m-%d') + "-" + str(date_start.hour))  # 日期转字符串存入列表
    return date_list




if __name__ == '__main__':
    print(create_date(date_start='2019-02-1-10', date_end='2019-02-1-10'))