from lianjiaSpider.item.zufang import zufangItem
import scrapy
import re
from scrapy import Request
from lianjiaSpider.zone.city import cities
from scrapy_redis.spiders import RedisSpider
from lianjiaSpider.utils.InsertRedis import inserintota,inserintotc
from lianjiaSpider.settings import DEFAULT_REQUEST_HEADERS

class lianjiaSpider(RedisSpider):
    name = "lianjia_zufang"
    # start_urls = ['https://www.lianjia.com/city/']
    redis_key = 'lianjia_zufang:start_urls'
    allowed_domains = ['lianjia.com']


    def parse(self, response):
        # 获取城市
        city_url_list = response.xpath("//div[@class='city_province']//li/a/@href").extract()
        city_name_list = response.xpath("//div[@class='city_province']//li/a/text()").extract()
        for index in range(len(city_name_list)):
            city_name = city_name_list[index]
            city_url = city_url_list[index]
            # 城市首字母
            city_alp = re.findall(r"https://(\w*).", city_url)[0]
            # 拼接城市租房url
            city_url = "https://" + city_alp + ".lianjia.com/zufang/"
            yield Request(url=city_url,callback=self.get_area_url)

    # 解析每个城市租房url
    def get_area_url(self, response):
        # 获取城区url
        area_url_list = response.xpath("//li[@data-type='district'][position()>1]/a/@href").extract()
        for area_url in area_url_list:
            area_url = re.findall(r"(.*)/zufang/", response.url)[0] + area_url
            yield scrapy.Request(url=area_url, callback=self.get_business_url)

    def get_business_url(self, response):
        # 获取商圈url
        business_url_list = response.xpath("//li[@data-type='bizcircle'][position()>1]/a/@href").extract()
        for business_url in business_url_list:
            business_url = re.findall(r"(.*)/zufang/", response.url)[0] + business_url

            yield scrapy.Request(url=business_url, callback=self.get_page_url)

    def get_page_url(self, response):
        # 获取最大页码
        max_page = response.xpath("//div[@class='content__pg']/@data-totalpage").extract()
        max_page = int(max_page[0]) if max_page else 0
        # print(max_page)
        # 遍历最大页 拼接完整的page_url
        # ---------page=0时 不会执行下面----------
        for page in range(max_page):
            page_url = response.url + "pg{}/#contentList".format(page + 1)
            yield scrapy.Request(url=page_url, callback=self.get_page_data)

    def get_page_data(self, response):
        zufang_xml_list = response.xpath("//div[@class='content__list']/div")
        city = response.xpath("//*[@id='content']/div[1]/p/a[1]/text()").extract()[0]
        for zufang_xml in zufang_xml_list:
            title = zufang_xml.xpath(".//p[@class='content__list--item--title twoline']/a/text()").extract()[0].strip()
            price = zufang_xml.xpath(".//em/text()").extract()[0]
            district = zufang_xml.xpath(".//p[@class='content__list--item--des']/a[1]/text()").extract()[0]
            microdistrict = zufang_xml.xpath(".//p[@class='content__list--item--des']/a[2]/text()").extract()[0]
            community = zufang_xml.xpath(".//p[@class='content__list--item--des']/a[3]/text()").extract()[0]
            item = zufangItem()
            item["title"] = title
            item["price"] = price
            item["district"] = district
            item["microdistrict"] = microdistrict
            item["community"] = community
            item["city"] = city
            yield item






