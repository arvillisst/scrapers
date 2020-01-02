# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class VcRuNewSpider(scrapy.Spider):
    name = 'vc_ru_new'
    allowed_domains = ['www.vc.ru']
    start_urls = ['https://vc.ru/new/']

    def parse(self, response):
        url_list = response.xpath('//div[@class="feed__container"]/div/div[@class="feed__item"]//a[@class="content-feed__link"]/@href').extract()
        for url in url_list:
            yield response.follow(url, callback=self.detail_info)

    def detail_info(self, response):
        title = response.url#.xpath('//h1[@class="content-header__title"]')
        print(title)



