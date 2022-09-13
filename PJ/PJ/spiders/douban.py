import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from ..items import DoubanItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']

    def start_requests(self):
        for page in range(10):
            yield Request(url=f'https://movie.douban.com/top250?start={page * 25}')

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        movie_items = sel.css('#content > div > div.article > ol > li')
        for movie_item in movie_items:
            item = DoubanItem()
            item['title'] = movie_item.css('span.title::text').extract_first()
            item['score'] = movie_item.css('span.rating_num::text').extract_first()
            item['quote'] = movie_item.css('span.inq::text').extract_first()
            yield item
