# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

#
import pandas as pd
import datetime


class HuodongjiaPipeline(object):
    def __init__(self):
        self.f = open("huodongjia.json", "w", encoding='utf-8')
        self.df = pd.DataFrame(columns=["会议", "日期", "地点", "行业"])

    def process_item(self, item, spider):
        # 删除每一次爬取的表头
        item['date'] = item['date'][:]
        item['place'] = item['place'][1:]
        item['industry'] = item['industry'][1:]
        df_temp = pd.DataFrame({"会议": item['meeting'],
                                "日期": item['date'],
                                "地点": item['place'],
                                "行业": item['industry']})
        self.df = self.df.append(df_temp)
        self.df["日期"] = pd.to_datetime(self.df["日期"])  # 将日期的字符串转为日期格式
        self.df = self.df[(self.df["日期"] >= self.get_next_week()[0]) & (
            self.df["日期"] <= self.get_next_week()[1])]  # 筛选出本下周的活动
        if len(df_temp) == 0:
            spider.crawler.engine.close_spider(spider)

        # 将日期类型转为字符串，否则excel打开之后会自动变为yyyy-mm-dd hh-mm-ss
        self.df["日期"] = self.df["日期"].apply(lambda x: x.strftime('%Y-%m-%d'))
        self.df.to_excel(
            f"{str(self.get_next_week()[0])}~{str(self.get_next_week()[1])}_huodongjia.xlsx",
            index=0,
            encoding='gb2312')

        return item

    def get_next_week(self):
        monday, sunday = datetime.date.today(), datetime.date.today()
        one_day = datetime.timedelta(days=1)
        seven_days = datetime.timedelta(days=7)
        while monday.weekday() != 0:
            monday -= one_day
        while sunday.weekday() != 6:
            sunday += one_day
        # 返回当前的星期一和星期天的日期
        return monday + seven_days, sunday + seven_days
