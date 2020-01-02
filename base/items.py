# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaseItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    base_image = scrapy.Field()
    rubric = scrapy.Field()
    created_at = scrapy.Field()
    pod_title = scrapy.Field()
    tags = scrapy.Field()
    text_content = scrapy.Field()


class GagadgetItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    image = scrapy.Field()
    categories = scrapy.Field()
    created_at = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

class FerraItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    image = scrapy.Field()
    category = scrapy.Field()
    created_at = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
