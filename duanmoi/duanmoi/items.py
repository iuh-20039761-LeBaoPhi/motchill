# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DuanmoiItem(scrapy.Item):
   
    coursename = scrapy.Field()
    trangthai = scrapy.Field()
    daodien = scrapy.Field()
    thoiluong = scrapy.Field()
    sotap = scrapy.Field()
    ngonngu = scrapy.Field() # add new
    namsx = scrapy.Field() # add new
    quocgia = scrapy.Field() # add new
    theloai = scrapy.Field() # add new
    mota = scrapy.Field() # add new
    courseUrl = scrapy.Field() # add new
    pass
