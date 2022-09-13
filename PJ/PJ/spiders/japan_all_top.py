import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from ..items import TopItem


class JapanAllTopSpider(scrapy.Spider):
    name = 'japan_all_top'
    allowed_domains = ['mamanoko.jp']
    start_urls = ['https://mamanoko.jp/']

    def parse(self, response, **kwargs):
        sel = Selector(response)
        top_list = sel.css('body > div.row > div.column.column-300px > ul:nth-child(4) > li')
        for top in top_list:
            item = TopItem()
            item['title'] = top.css('div > div.list_view-content > a::text').extract_first()
            item['view'] = top.css('span::text').extract_first()
            item['editorial'] = top.css('span.is-right::text').extract_first()
            yield item
