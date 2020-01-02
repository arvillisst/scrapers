# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from base.items import FerraItem

class FerraSpider(scrapy.Spider):
    name = 'ferra'
    allowed_domains = ['ferra.ru']
    start_urls = ['https://www.ferra.ru/news']

    def parse(self, response):
        urls = response.xpath('//a[@class="jsx-2419072339 link jsx-1968532000 link"]/@href').getall()
        for url in urls:
            # print(response.follow(url))
            yield response.follow(url, callback=self.get_detail)

        next_page = response.xpath('//a[@class="jsx-2419072339 link"]/@href').get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def get_detail(self, response):
        item = FerraItem()
        category = response.xpath('//a[@class="jsx-1049894682 link"]/text()').get()
        item['category'] = category

        title = response.xpath('//h1[@class="jsx-1660569506 jsx-2918605334 heading jsx-19050688 headline"]/text()').get().strip()
        item['title'] = title

        image = response.xpath('//link[@itemprop="url"]/@href').get()
        item['image_urls'] = [response.urljoin(response.xpath('//link[@itemprop="url"]/@href').get())]

        created_at = response.xpath('//div[@class="jsx-3590770510 time"]/div/text()').get()
        item['created_at'] = created_at

        tags = response.xpath('//div[@class="jsx-974541726 jsx-506205320 tags desktop"]//span[@class="jsx-654120458 _3YCPwdvnClaIvQgy_oX0QM"]/text()').getall()
        item['tags'] = tags

        soup = BeautifulSoup(response.text, 'lxml')
        # print(response.url)
        txt1 = soup.find('div', class_='jsx-420534269 lead').get_text()
        txt2 = soup.find('div', class_='jsx-736142825 text _3KxCb2trUGpayFjLkeXcq-').get_text()

        content = txt1 + txt2
        item['content'] = content
        yield item
