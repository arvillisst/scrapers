# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import re
from bs4 import BeautifulSoup

from base.items import GagadgetItem

class GagadgetSpider(scrapy.Spider):
    name = 'gagadget'
    allowed_domains = ['gagadget.com']
    start_urls = ['https://gagadget.com/news/']

    def parse(self, response):
        uls = response.xpath('//ul[@class="unstyled alphabet"]//li[@class="bottom2"]/a/@href').getall()
        for url in uls:
            # print(SplashRequest(response.urljoin(url)))
            yield response.follow(url, callback=self.get_detail_category)
            # yield SplashRequest(response.urljoin(url), callback=self.get_detail_category, args={'wait': 1.0})

    def get_detail_category(self, response):
        grid = response.xpath('//span[@class="cell-title"]/a/@href').getall()

        for url in grid:
            # print('==========> ', response.urljoin(url))
            yield response.follow(url, callback=self.get_detail_info)

    def get_detail_info(self, response):
        item = GagadgetItem()

        categories = response.xpath('//ul[@class="breadcrumbs bottom10"]/li/a/text()').getall()
        item['categories'] = categories

        title = response.xpath('//div[@class="b-nodetop b-nodetop_nobor"]/h1/text()').get().strip()
        item['title'] = title

        image = response.urljoin(response.xpath('//img[@class="js-album"]/@src').get())

        item['image_urls'] = [response.urljoin(response.xpath('//img[@class="js-album"]/@src').get())]

        # content = response.xpath('//div[@class="b-font-def post-links"]//p').getall()
        soup = BeautifulSoup(response.text, 'lxml')
        # print(response.url)
        txt = soup.find('div', class_='b-font-def post-links').find_all('p')
        tmp_content = []
        for i in txt:
            tmp_content.append(i.text)
            # print(i.text)
        item['content'] = tmp_content

        # print(response.url, title, content)
        tags = response.xpath('//div[@class="b-node-author top20"]//a/text()').getall()
        item['tags'] = tags

        created_at = response.xpath('//div[@class="bottom10 pull-left"]/text()')[1].extract()
        item['created_at'] = created_at
        # print(tags, created_at)

        yield item

