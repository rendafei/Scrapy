# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # 爬取电影标题
    score = scrapy.Field()  # 爬取电影评分
    quote = scrapy.Field()  # 爬取电影金句


class BabyItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    view = scrapy.Field()  # 访问量
    editorial = scrapy.Field()  # 编辑部
    image = scrapy.Field()  # 标题图片
    introduction = scrapy.Field()  # 文章简介
    catalogue = scrapy.Field()  # 文章目录
    label = scrapy.Field()  # 文章标签
    content = scrapy.Field()  # 文章内容
    content_image = scrapy.Field()  # 文章插图
    s_paragraph = scrapy.Field()  # 二级段落标题
    t_paragraph = scrapy.Field()  # 三级段落标题


class TopItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    view = scrapy.Field()  # 访问量
    editorial = scrapy.Field()  # 编辑部


class NewsItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    view = scrapy.Field()  # 访问量
    editorial = scrapy.Field()  # 编辑部
