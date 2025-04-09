import scrapy


class Crawlm3U8DataItem(scrapy.Item):
    url = scrapy.Field()
