import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from ..items import BabyItem


class JapanSpider(scrapy.Spider):
    name = 'japan'
    allowed_domains = ['mamanoko.jp']

    def start_requests(self):
        for index in range(1, 2):
            yield Request(url=f'https://mamanoko.jp/?page={index}')

    def parse(self, response, **kwargs):
        sel = Selector(response)
        baby_messages = sel.css('body > div.row > div.column.column-440px > ul > li')
        for message in baby_messages:
            item = BabyItem()
            item['title'] = message.css('h3 > a::text').extract_first()
            item['view'] = message.css('span::text').extract_first()
            item['editorial'] = message.css('span.is-right::text').extract_first()
            item['image'] = message.css('a > img::attr(data-original)').extract_first()
            yield Request(url=f'https://mamanoko.jp/' + message.css('h3 > a::attr(href)').extract_first(),
                          callback=self.detail_parse,
                          cb_kwargs={'item': item})
            # yield item

    def detail_parse(self, response, **kwargs):
        sel = Selector(response)
        detail_informations = sel.css('#article > main > article')
        for information in detail_informations:
            detail_item = kwargs['item']
            detail_item['label'] = information.css('header > ul > li > a::text').extract()
            detail_item['introduction'] = information.css('header > p::text').extract_first()
            detail_item['catalogue'] = information.css('section.c-tableOfContents > ol > li > a::text').extract()
            article = information.xpath("//section[@class='p-articleItems']")
            for del_element in article.xpath('//div[@class="c-articles_items_product"]'):
                # 这里必须定位至父节点删除子节点，不允许“自杀”
                del_element.getparent()
            detail_item['content'] = article.xpath(
                "string(//section[@class='p-articleItems'])").extract()
            # detail_item['content'] = information.css('section.p-articleItems > div > p::text').extract()
            # detail_item['content_image'] = information.css(
            #     'section.p-articleItems > div > img::attr(data-original)').extract()
            # detail_item['s_paragraph'] = information.css('section.p-articleItems > div > h2::text').extract()
            # detail_item['t_paragraph'] = information.css('section.p-articleItems > div > h3::text').extract()
            yield detail_item
# xpath('string(//h2|//h3|//p)').
