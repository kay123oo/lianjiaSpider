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
    redis_key = 'lianjia_zufang:start_urls'
    allowed_domains = ['gz.lianjia.com',
                       'bj.lianjia.com',
                       'sz.lianjia.com',
                       'sh.lianjia.com'
                       ]

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
        area_name_list = response.xpath("//li[@data-type='district'][position()>1]/a/text()").extract()
        for area_url ,area_name in zip(area_url_list ,area_name_list):
            area_url = re.findall(r"(.*)/zufang/", response.url)[0] + area_url
            yield scrapy.Request(url=area_url, callback=self.get_business_url,meta={"area_name": area_name})

    def get_business_url(self, response):
        # 获取商圈url
        area_name = response.meta["area_name"]
        business_url_list = response.xpath("//li[@data-type='bizcircle'][position()>1]/a/@href").extract()
        business_name_list = response.xpath("//li[@data-type='bizcircle'][position()>1]/a/text()").extract()
        for business_url, business_name in zip(business_url_list, business_name_list):
            business_url = re.findall(r"(.*)/zufang/", response.url)[0] + business_url
            yield scrapy.Request(url=business_url, callback=self.get_page_url, meta={"business_name": business_name,
                                                                                     "area_name":area_name})

    def get_page_url(self, response):
        area_name = response.meta["area_name"]
        business_name = response.meta["business_name"]
        # 获取最大页码
        max_page = response.xpath("//div[@class='content__pg']/@data-totalpage").extract()
        max_page = int(max_page[0]) if max_page else 0
        # print(max_page)
        # 遍历最大页 拼接完整的page_url
        # ---------page=0时 不会执行下面----------
        for page in range(max_page):
            page_url = response.url + "pg{}/#contentList".format(page + 1)
            yield scrapy.Request(url=page_url, callback=self.get_page_data, meta={"business_name": business_name,
                                                                                  "area_name": area_name})

    def get_page_data(self, response):
        area_name = response.meta["area_name"]
        business_name = response.meta["business_name"]
        zufang_xml_list = response.xpath("//div[@class='content__list']/div")
        city = response.xpath("//*[@id='content']/div[1]/p/a[1]/text()").extract()[0]
        for zufang_xml in zufang_xml_list:
            try:
                item = zufangItem()
                title = zufang_xml.xpath(".//p[@class='content__list--item--title twoline']/a/text()").extract()[0].strip()
                price = zufang_xml.xpath(".//em/text()").extract()[0]
                dataDistributionType = zufang_xml.xpath(".//@data-distribution_type").extract()[0]
                # 获取详情页
                detail_url =zufang_xml.xpath(".//p[@class='content__list--item--title twoline']/a/@href").extract()[0]
                detail_url = "https://bj.lianjia.com" + detail_url

                if dataDistributionType == '203500000002':
                    print(int(dataDistributionType))
                    item["district"] = area_name
                    item["microdistrict"] = business_name
                    item['dataDistributionType'] = 1
                    if zufang_xml.xpath(".//span[@class='room__left']").extract():
                        item["area"]= zufang_xml.xpath(".//p[@class='content__list--item--des']/text()[3]").extract()[0]
                        item["houseType"] = zufang_xml.xpath(".//p[@class='content__list--item--des']/text()[5]").extract()[0]
                    else:
                        item["area"]  = zufang_xml.xpath(".//p[@class='content__list--item--des']/text()[1]").extract()[0]
                        item["houseType"] = zufang_xml.xpath(".//p[@class='content__list--item--des']/text()[3]").extract()[0]
                elif dataDistributionType == '203500000001':
                    item['dataDistributionType'] = 0
                    item["district"] = zufang_xml.xpath(".//p[@class='content__list--item--des']/a[1]/text()").extract()[0]
                    item["microdistrict"] = zufang_xml.xpath(".//p[@class='content__list--item--des']/a[2]/text()").extract()[0]
                    item["community"] = zufang_xml.xpath(".//p[@class='content__list--item--des']/a[3]/text()").extract()[0]
                    item["area"] = zufang_xml.xpath(".//p[@class='content__list--item--des']/text()[5]").extract()[0].strip()
                    item["orientation"] = zufang_xml.xpath(".//p[@class='content__list--item--des']/text()[6]").extract()[0].strip()
                    item["houseType"] = zufang_xml.xpath(".//p[@class='content__list--item--des']/text()[7]").extract()[0].strip()
                tags_xml = zufang_xml.xpath(".//p[@class='content__list--item--bottom oneline']/i/text()").extract()
                tags =[]
                if(tags_xml):
                    for tag in tags_xml:
                        tags.append(tag)
                    item['tags'] = tags
                item["title"] = title
                item["price"] = price
                item["city"] = city
            except Exception as e:
                print(e)
                yield scrapy.Request(url=detail_url, callback=self.get_item_detail, meta={"data": item},
                                     dont_filter=True)

    def get_item_detail(self, response):
        item = response.meta["data"]
        try:
            lon_lat_str = response.xpath("//*[@class='map__cur']/@data-coord").extract()[0]
            pa_lon = r"\"longitude\":\"(.*)\","
            pa_lat = r"\"longitude\":\"(.*)\","
            item['longitude'] = re.findall(pa_lon, lon_lat_str)[0]
            item['latitude'] = re.findall(pa_lat, lon_lat_str)[0]
            distance = response.xpath("//*[@class='map--overlay__list--title']/span").extract()
            item['floor'] = response.xpath("//div[@class='content__article__info']/ul/li[8]/text()").extract()
            if len(distance) > 0:
                item['distance']= distance[0]
            else:
                item['distance']= None
        except Exception as e:
            print(e)
            item['longitude'] = None
            item['latitude'] = None
            item['distance'] = None
        yield item









