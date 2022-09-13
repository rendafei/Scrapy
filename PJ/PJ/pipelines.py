# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
"""此文件用来写，爬虫工作的钩子函数。及爬虫在工作时自动回调的函数"""
import openpyxl
import pymysql

from .items import DoubanItem

"""单处理录入数据库"""

# class DoubanSqlItemPipeline:
#     def __init__(self):
#         self.conn = pymysql.connect(host='127.0.0.1', user='root', password='mengdong123', database='pj', port=3306)
#
#     def process_item(self, item: DoubanItem, spider):
#         """生成可执行SQL语句对象db"""
#         db = self.conn.cursor()
#         db.execute(
#             'insert into movie (mov_title,mov_score,mov_quote) values (%s,%s,%s)', (
#                 item['title'], item['score'], item['quote'])
#         )
#         """将SQL语句同步数据库"""
#         self.conn.commit()
#         return item
#
#     def close_spider(self, spider):
#         self.conn.close()
"""批次录入数据库"""


class DoubanSqlItemPipeline:
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='mengdong123', database='pj', port=3306)
        self.data = list()
        self.db = self.conn.cursor()

    def process_item(self, item: DoubanItem, spider):
        """生成可执行SQL语句对象db"""
        self.data.append((item['title'], item['score'], item['quote']))
        if len(self.data) == 100:
            self._write_to_sql()
            """将SQL语句同步数据库"""
            self.conn.commit()
            self.data.clear()
        return item

    def _write_to_sql(self):
        self.db.executemany(
            'insert into movie (mov_title,mov_score,mov_quote) values (%s,%s,%s)',
            self.data)

    def close_spider(self, spider):
        if len(self.data) > 0:
            self._write_to_sql()
        self.conn.close()


class DoubanExcelItemPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.sheet = self.wb.active
        self.sheet.title = "Top250"
        self.sheet.append(('名称', '评分', '金句'))

    """爬虫工作时，数据的处理函数"""

    def process_item(self, item: DoubanItem, spider):
        self.sheet.append((item['title'], item['score'], item['quote']))
        return item

    """爬虫启动时，钩子函数"""

    def open_spider(self, spider):
        print('爬虫开始')

    """爬虫结束时，钩子函数"""

    def close_spider(self, spider):
        self.wb.save('Top250_数据.xlsx')
        print('爬虫结束')
