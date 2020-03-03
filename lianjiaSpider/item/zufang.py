from scrapy.item import Item ,Field


class zufangItem(Item):
    # 租房信息标题
    title = Field()
    # 租金
    price = Field()
    # 房屋面积
    area = Field()
    # 所在城市
    city = Field()
    # 所在区县
    district = Field()
    # 所在商圈
    microdistrict = Field()
    # 所在小区
    community = Field()
    # 房屋类型：个人房源或公寓
    dataDistributionType = Field()
    # 个人房源类型：合租或整租
    rentType = Field()
    # 房源标签
    tags = Field()
    # 朝向
    orientation = Field()
    # 户型
    houseType = Field()
    # 几厅
    hall_num = Field()
    # 几室
    bedroom_num = Field()
    # 几卫
    bathroom_num = Field()
    # 经度
    longitude = Field()
    # 纬度
    latitude = Field()
    # 距离地铁站距离
    distance = Field()


