# -*- coding: utf-8 -*-
import scrapy
from twisted.internet import reactor
from twisted.internet import task
from scrapy.crawler import CrawlerRunner


class GelbeseSpider(scrapy.Spider):
    name = 'gelbese'
    allowed_domains = ['gelbeseiten.de']
    ## 'https://www.gelbeseiten.de/Suche/Treppenlift/Bundesweit', 'https://www.gelbeseiten.de/Suche/Aufz%C3%BCge/Bundesweit'
    start_urls = ['https://www.gelbeseiten.de/Suche/H%C3%B6rger%C3%A4te/Bundesweit',
                  ]

    def parse(self, response):
        urls = response.xpath('//article[@class="mod mod-Treffer"]/a/@href').getall()
        # print(len(urls))
        for url in urls:
            # print(url)
            yield response.follow(url, callback=self.get_detail_info)
            break

        next_page = response.xpath('//a[@class="gs_paginierung__sprungmarke gs_paginierung__sprungmarke--vor btn btn-default"]/@href').get()
        # print(next_page)

    def get_detail_info(self, response):
        '''
        2.1. postcode (Plz)
        2.2. name
        2.3. street
        2.4. city
        2.5. phone
        2.6. fax
        2.7. facebook Page
        2.8. email
        2.9. website
        2.10. opening times - Array of Values (Öffnungszeiten)
        2.11. branch (Branche)
        2.12. CEO (Geschäftsführer or Inhaber)
        2.13. memberships - Array of Values (Mitgliedschaften)
        2.14. operating area - Array of Values (Aktionsradien)
        2.15. raw_content (complete code of the scraped HTML Website without Linebreaks - minify 1 line)
        2.16. Url (the URL of the scraped website)
 '''
        url = response.url
        name = response.xpath('//h1[@class="mod-TeilnehmerKopf__name"]/text()').get()
        street = response.xpath('//span[@property="streetAddress"]/text()').get()
        city = response.xpath('//span[@property="addressLocality"]/text()').get()
        post_code = response.xpath('//span[@property="postalCode"]/text()').get()
        phone = response.xpath('//a[@class="nolink-black"]/span/text()').get()
        website = response.xpath('//li[@class="mod-Kontaktdaten__list-item :: link-blue"]//i[@class="icon-homepage"]/following-sibling::span/text()').get()
        if website:
            existing_website = website
            # print(website)
        fax = response.xpath('//span[@property="faxnumber"]/text()').get()
        if fax:
            existing_fax = fax
            # print(fax)
        # opening_times = response.xpath('//table[@class="mod-Oeffnungszeiten__table"]//tr')
        # print(opening_times)
        print(url, name, street)


def run_crawl():
    """
    Run a spider within Twisted. Once it completes,
    wait 5 seconds and run another spider.
    """
    runner = CrawlerRunner()
    runner.crawl(GelbeseSpider)
#     deferred = runner.crawl(GelbeseSpider)
#     # you can use reactor.callLater or task.deferLater to schedule a function
#     deferred.addCallback(reactor.callLater, 5, run_crawl)
#     return deferred
#
# run_crawl()
# reactor.run()   # you have to run the reactor yourself
l = task.LoopingCall(run_crawl)
l.start(10)
reactor.run()