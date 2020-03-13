from django.shortcuts import render
from django.views import generic
from .models import zufang
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page
from .utils.district_and_microdistrict import DM ,ZH_EN
from .utils.pinyin_util import pinyin
from django.core.cache import cache #引入缓存模块
from .utils.const import const
from mongoengine.queryset.visitor import Q
import re

# Create your views here.

# 用于获取数据库中model的列表
class IndexView(generic.ListView):
    template_name = "Mainapp/index2.html"      # 需要渲染的模板
    context_object_name = "houses"           # 模板中使用的上下文变量

    def get_queryset(self):
        return zufang.objects.all()[:10]

def sort_by_cons(request, city, district,microdistrict,conditions):
    return render(request, 'Mainapp/index2.html')

def index(request):
    return render(request, 'Mainapp/base.html')

@cache_page(60 * 10)
def group_by_city(request, city):
    city_zh = get_city_by_abbr(city)
    zufang_list = zufang.objects(city=city_zh)
    total_count= len(zufang_list)
    districts = DM.get(str(city_zh))
    paginator = Paginator(zufang_list, 30)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)

    except PageNotAnInteger:
        # 如果请求的页数不是整数，返回第一页。
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        contacts = paginator.page(paginator.num_pages)

    data = {
        # 页数据
        'contacts': contacts ,
        # 总数据项数量
        'total_count': total_count,
        # 当前城市的区县
        'districts' : districts,
        'current_city': {'abbr': city, 'zh': city_zh}

    }

    return render(request, 'Mainapp/index2.html', data)

@cache_page(60 * 10)
def group_by_district(request, city, district):
    print("group_by_district！！！！！")

    district_zh = ZH_EN.get(district)
    city_zh = get_city_by_abbr(city)
    # 获取区县
    districts = DM.get(str(city_zh))
    # 或许该区县的所有数据
    result_list = zufang.objects(district=district_zh)
    total_count = len(result_list)
    # 返回该区县下的商圈
    microdistricts = DM.get(str(district_zh))
    # 分页
    paginator = Paginator(result_list, 30)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)

    except PageNotAnInteger:
        # 如果请求的页数不是整数，返回第一页。
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        contacts = paginator.page(paginator.num_pages)

    data = {
        # 页数据
        'contacts': contacts,
        # 总数据项数量
        'total_count': total_count,
        # 当前区县的商圈
        'microdistricts': microdistricts ,

        'current_city': {'abbr':city,'zh':city_zh} ,

        'current_district': {'en':district,'zh':district_zh},

        'districts':districts

    }
    return render(request, 'Mainapp/index2.html', data)

@cache_page(60 * 10)
def group_by_microdistrict(request, city, district,microdistrict):
    print("group_by_microdistrict！！")
    district_zh = ZH_EN.get(district)
    city_zh = get_city_by_abbr(city)
    # 获取区县
    districts = DM.get(str(city_zh))
    # 返回该区县下的商圈
    microdistricts = DM.get(str(district_zh))
    microdistrict_zh = ZH_EN.get(microdistrict)
    print(microdistrict_zh)
    result_list =  zufang.objects(microdistrict= microdistrict_zh)
    Q1= Q(price__gte=100000 ) | Q(price__lte=4000 )
    Q2= Q(area__gte=100)
    res =  zufang.objects((Q1 & Q2))
    total_count = len(result_list)
    # 分页
    paginator = Paginator(result_list, 30)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)

    except PageNotAnInteger:
        # 如果请求的页数不是整数，返回第一页。
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        contacts = paginator.page(paginator.num_pages)

    data = {
        # 页数据
        'contacts': contacts,
        # 总数据项数量
        'total_count': total_count,
        # 当前区县的商圈
        'microdistricts': microdistricts,

        'current_city': {'abbr': city, 'zh': city_zh},

        'current_district': {'en':district,'zh':district_zh},

        'current_microdistrict': microdistrict_zh,

        'districts': districts
    }
    return render(request, 'Mainapp/index2.html', data)

'''
    出租方式：整租rt0，合租rt1，公寓rt2
    租金：rp
    户型：ht
    面积：ra
    朝向：or
    楼层：lc
    电梯：dt
'''


def get_by_conditions(request,  conditions, city, district="", microdistrict=""):
    rent_type = re.findall(r'rt([0-9])', conditions)
    resQ = Q()
    if rent_type:
        resQ = getQ_by_rent_type(rent_type)
    prices_conditions = re.findall(r'rp([0-9])', conditions)
    if prices_conditions:
        resQ = (resQ | getQ_by_rp(prices_conditions))

    house_type_conditions = re.findall(r'ht([0-9])', conditions)
    if house_type_conditions:
        resQ = (resQ | getQ_by_house_tyoe(house_type_conditions))

    area_conditions = re.findall(r'ra([0-9])', conditions)

    orientation_conditions = re.findall(r'or([0-9])', conditions)
    if orientation_conditions:
        resQ = (resQ | getQ_by_orientation(orientation_conditions))
    floor_conditions = re.findall(r'lc([0-9])', conditions)

    city_zh = get_city_by_abbr(city)
    district_zh = ZH_EN.get(district)
    microdistrict_zh = ''
    if microdistrict:
        microdistrict_zh = ZH_EN.get(microdistrict)
        resQ = (resQ & Q(microdistrict=microdistrict_zh))
    elif district :
        resQ = (resQ & Q(district=district_zh))
    districts = DM.get(str(city_zh))
    microdistricts = DM.get(str(district_zh))
    result_list = zufang.objects(resQ)
    total_count = len(result_list)
    # 分页
    paginator = Paginator(result_list, 30)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)

    except PageNotAnInteger:
        # 如果请求的页数不是整数，返回第一页。
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        contacts = paginator.page(paginator.num_pages)

    data = {
        # 页数据
        'contacts': contacts,
        # 总数据项数量
        'total_count': total_count,
        # 当前区县的商圈
        'microdistricts': microdistricts,

        'current_city': {'abbr': city, 'zh': city_zh},

        'current_district': {'en': district, 'zh': district_zh},

        'current_microdistrict': microdistrict_zh,

        'districts': districts ,

        'current_conditions' : conditions
    }
    return render(request, 'Mainapp/index2.html', data)




def get_city_by_abbr(abbr):
    city=''
    if abbr == 'sz':
        city = '深圳'
    elif abbr == 'bj':
        city = '北京'
    elif abbr == 'sh':
        city = '上海'
    elif abbr == 'gz':
        city = '广州'
    return city


def getQ_by_rp(prices):
    resQ=Q()
    for price in prices:
        if int(price) == const.PRICE_00:
            resQ = resQ | Q(price__lte=1000 )
        elif int(price) == const.PRICE_01:
            resQ = resQ | (Q(price__gt=1000) & Q(price__lte=1500) )
        elif int(price) == const.PRICE_02:
            resQ = resQ | (Q(price__gt=1500) & Q(price__lte=2000))
        elif int(price) == const.PRICE_03:
            resQ = resQ | (Q(price__gt=2000) & Q(price__lte=2500))
        elif int(price) == const.PRICE_04:
            resQ = resQ | (Q(price__gt=2500) & Q(price__lte=3000))
        elif int(price) == const.PRICE_05:
            resQ = resQ | (Q(price__gt=3000) & Q(price__lte=5000))
        elif int(price) == const.PRICE_06:
            resQ = resQ | (Q(price__gte=5000))
    return resQ


def getQ_by_rent_type(rentTypes):
    resQ=Q()
    for rentType in rentTypes:
        print(rentType)
        if int(rentType) == const.RENT_TYPE_00:
            resQ = Q(dataDistributionType=0)
        elif int(rentType) == const.RENT_TYPE_01:
            resQ = (resQ | Q(dataDistributionType=1))
    return resQ

def getQ_by_house_tyoe(houseTypes):
    resQ=Q()
    for ht in houseTypes:
        ht = int(ht)
        if ht == const.HOUSE_TYPE_00:
            resQ = resQ | Q(hall_num=1)
        elif ht == const.HOUSE_TYPE_01:
            resQ = resQ | Q(hall_num=2)
        elif ht == const.HOUSE_TYPE_02:
            resQ = resQ | Q(hall_num=3)
        elif ht == const.HOUSE_TYPE_03:
            resQ = resQ | Q(hall_num__gte=4)
    return resQ


def getQ_by_orientation(orientations):
    resQ=Q()
    for o in orientations:
        o = int(o)
        if o == const.ORIENTATION_00:
            resQ = resQ | Q(orientation='东')
        elif o == const.ORIENTATION_01:
            resQ = resQ | Q(orientation='南')
        elif o == const.ORIENTATION_02:
            resQ = resQ | Q(orientation='西')
        elif o == const.ORIENTATION_03:
            resQ = resQ | Q(orientation='北')
        elif o == const.ORIENTATION_03:
            resQ = resQ | Q(orientation='南北')
    return resQ




