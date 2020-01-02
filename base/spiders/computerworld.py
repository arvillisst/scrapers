# -*- coding: utf-8 -*-
import scrapy
from base.items import BaseItem

class ComputerworldSpider(scrapy.Spider):
    name = 'computerworld'
    allowed_domains = ['www.computerworld.ru']
    start_urls = ['https://www.computerworld.ru/news']

    def parse(self, response):
        urls = response.xpath('//div[@class="article-list row news-list"]//h3/a/@href').getall()

        for url in urls:
            yield response.follow(url, callback=self.detail_info)
            # print(response.follow(url))
            # break

        next_page = response.xpath('//ul[@class="pagination"]//li/a/@href').getall()[-2]

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def detail_info(self, response):
        item = BaseItem()
        item['title'] = response.xpath('//h1/text()').get()
        try:
            item['base_image'] = 'https://www.computerworld.ru' + response.xpath('//div[@class="thumbnail  fl mb10 mr10"]/img/@src').get()
        except:
            pass
        item['rubric'] = response.xpath('//span[@class="label tag rubric"]/text()').get()
        item['created_at'] = response.xpath('//p[@class="fl"]/text()').get().strip()
        item['pod_title'] = response.xpath('//p[@class="lead"]/text()').get().strip()
        item['tags'] = response.xpath('//div[@class="row article-full"]//a[@class="visible tag-link"]/span[@class="label tag "]/text()').getall()
        # print(title, pod_title, rubric, )
        content = response.xpath('//article[@class="js-mediator-article"]//p/text()').getall()
        tmp_content = []
        for c in content:
            tmp_content.append(c)

            # print(c)
        item['text_content'] = tmp_content

        yield item
