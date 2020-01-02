# -*- coding: utf-8 -*-
import scrapy


class InnotechtodaySpider(scrapy.Spider):
    name = 'innotechtoday'
    allowed_domains = ['www.innotechtoday.com']
    start_urls = ['https://innotechtoday.com/']

    def parse(self, response):
        uls = response.xpath('//ul[@id="mega-menu-header-menu"]//li')

        for li in uls:
            urls = li.xpath('//a[@class="mega-menu-link"]/@href').getall()

            for url in urls:
                yield response.follow(url, callback=self.parse_category_page)
                # print(response.follow(url))
            break

    def parse_category_page(self, response):
        urls = response.xpath('//div[@class="row bottom-margin"]').getall()
        print(response)
        # for url in urls:
        #     print(url)


