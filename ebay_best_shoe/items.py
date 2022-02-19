# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class EbayBestShoeItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    shipping_price = scrapy.Field()
    total_price = scrapy.Field()
    product_link = scrapy.Field()
