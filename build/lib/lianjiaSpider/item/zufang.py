from scrapy.item import Item ,Field


class zufangItem(Item):
    # 租房信息名字
    title = Field()
    # 租金
    price = Field()
    # 房屋面积
    area = Field()
    # 所在城市
    city = Field()
    # 所在区县
    district = Field()
    # 所在区域
    microdistrict = Field()
    # 所在小区
    community = Field()
    # 房屋类型：个人房源或公寓
    houseType = Field()
    # 个人房源类型：合租或整租
    rentType = Field()

