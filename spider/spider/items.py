# -*- coding: utf-8 -*-
import scrapy


class House(scrapy.Item):
    title = scrapy.Field()
    imgs = scrapy.Field()
    bedroom = scrapy.Field()
    area = scrapy.Field()
    total_price = scrapy.Field()
    plot = scrapy.Field()
    type = scrapy.Field()
    unit_price = scrapy.Field()
    position = scrapy.Field()
    down_payment = scrapy.Field()
    year = scrapy.Field()
    direction = scrapy.Field()
    house_type = scrapy.Field()
    floor = scrapy.Field()
    decoration = scrapy.Field()
    property_year = scrapy.Field()
    elevator = scrapy.Field()
    house_year = scrapy.Field()
    property = scrapy.Field()
    heating = scrapy.Field()
    only = scrapy.Field()
    one_hand = scrapy.Field()
    core_point = scrapy.Field()
    owner_men = scrapy.Field()
    service_introduction = scrapy.Field()
    house_code = scrapy.Field()
    add_date = scrapy.Field()
