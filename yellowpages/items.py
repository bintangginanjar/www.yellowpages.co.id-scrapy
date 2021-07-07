# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Item, Field
from itemloaders.processors import MapCompose, TakeFirst, Join

class YellowpagesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bidang = Field()
    kategori = Field()
    pageUrl = Field()
    namaClient = Field()
    alamat = Field()
    kota = Field()
    noTelp = Field()
    email = Field()
    site = Field()

    pass
