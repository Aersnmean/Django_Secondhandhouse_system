# -*- coding: utf-8 -*-
import scrapy
from ..items import *
import requests


class Spider1PySpider(scrapy.Spider):
    name = 'anjuke'
    allowed_domains = ['ty.anjuke.com/']
    start_urls = ['https://ty.anjuke.com/sale/p{}/'.format(i) for i in range(51)]
    # start_urls = ['https://ty.anjuke.com/sale/p1/']

    # def start_requests(self):
        # yield scrapy.Request(url='https://ty.anjuke.com/sale/p1', callback=self.parse)

    def parse(self, response):
        houselist = response.xpath('//li[@class="list-item"]/div[@class="house-details"]/div[@class="house-title"]/a/@href').extract()
        for i in houselist:
            yield scrapy.Request(url=i, callback=self.parse1, dont_filter=True)
    def parse1(self, response):
        # 标题
        title = response.xpath('//h3[@class="long-title"]/txt()').extract()
        # 图片
        imgs = response.xpath('//div[@class="img_wrap"]/img/@data-src').extract()
        # print(imgs, type(imgs))
        # 房屋信息
        plot = response.xpath('//div[@class="houseInfo-content"][1]/a/txt()').extract()
        # print(plot)
        position = response.xpath('//p[@class="loc-txt"]/a/txt() | //p[@class="loc-txt"]/txt()[2]').extract()
        position[-1] = position[-1].replace('－', '').replace('\n ', '').replace('\t', '').replace(' ', '')
        bedroom = response.xpath('//span[@class="info-tag"]/em/txt()').extract()
        # print(house, position)
        houseinfo = response.xpath('//span[@class="light info-tag"]/em/txt()|\
                                            //li[@class="houseInfo-detail-item"]/div[@class="houseInfo-label txt-overflow"]/txt() |\
                                            //li[@class="houseInfo-detail-item"]/div[@class="houseInfo-content"]/txt()').extract()
        # print(houseinfo)
        # 房屋编码，发布时间
        housecode = response.xpath('//span[@id="houseCode"]/txt() | //span[@class="house-encode"]/txt()').extract()
        # print(housecode)
        houseinfodesc1 = response.xpath('//div[@class="houseInfo-item-desc js-house-explain"]/span/txt()').extract()
        houseinfodesc2 = response.xpath('//div[@class="houseInfo-item-desc"]/txt()').extract()
        # print(houseinfodesc1, houseinfodesc2)
        try:
            house = House()
            house['title'] = title[0].replace('\n ', '').strip(' ')
            house['imgs'] = imgs
            house['bedroom'] = bedroom[:-1]
            house['area'] = bedroom[-1]
            house['total_price'] = houseinfo[0]
            house['plot'] = plot[0]
            house['type'] = houseinfo[houseinfo.index('房屋户型：') + 1].replace('\t', '').replace(' ', '').split('\n')[1:-1] if '房屋户型：' in houseinfo else None
            house['unit_price'] = houseinfo[houseinfo.index('房屋单价：') + 1].split(' ')[0] if '房屋单价：' in houseinfo else None
            house['position'] = position
            house['down_payment'] = houseinfo[houseinfo.index('参考首付：') + 1].strip() if '参考首付：' in houseinfo else None
            house['year'] = houseinfo[houseinfo.index('建造年代：') + 1].strip() if '建造年代：' in houseinfo else None
            house['direction'] = houseinfo[houseinfo.index('房屋朝向：') + 1] if '房屋朝向：' in houseinfo else None
            house['house_type'] = houseinfo[houseinfo.index('房屋类型：') + 1] if '房屋类型：' in houseinfo else None
            house['floor'] = houseinfo[houseinfo.index('所在楼层：') + 1] if '所在楼层：' in houseinfo else None
            house['decoration'] = houseinfo[houseinfo.index('装修程度：') + 1] if '装修程度：' in houseinfo else None
            house['property_year'] = houseinfo[houseinfo.index('产权年限：') + 1] if '产权年限：' in houseinfo else None
            house['elevator'] = houseinfo[houseinfo.index('配套电梯：') + 1] if '配套电梯：' in houseinfo else None
            house['house_year'] = houseinfo[houseinfo.index('房本年限：') + 1] if '房本年限：' in houseinfo else None
            house['property'] = houseinfo[houseinfo.index('产权性质：') + 1] if '产权性质：' in houseinfo else None
            house['heating'] = houseinfo[houseinfo.index('配套供暖：') + 1] if '配套供暖：' in houseinfo else None
            house['only'] = houseinfo[houseinfo.index('唯一住房：') + 1] if '唯一住房：' in houseinfo else None
            house['one_hand'] = houseinfo[houseinfo.index('一手房源：') + 1] if '一手房源：' in houseinfo else None
            house['core_point'] = houseinfodesc1[0]
            house['owner_men'] = houseinfodesc2[0].strip()
            house['service_introduction'] = houseinfodesc2[1].strip()
            house['house_code'] = housecode[0].split('：')[-1].strip('，').strip()
            house['add_date'] = housecode[1].split('：')[-1]
            yield house
        except Exception as e:
            print(e)
