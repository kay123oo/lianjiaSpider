from django.shortcuts import render
from django.views import generic
from .models import zufang_sh
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pypinyin import pinyin
from django.views.decorators.cache import cache_page
from .utils.district_and_microdistrict import DM

from django.core.cache import cache #引入缓存模块

# Create your views here.

# 用于获取数据库中model的列表
class IndexView(generic.ListView):
    template_name = "Mainapp/test.html"      # 需要渲染的模板
    context_object_name = "houses"           # 模板中使用的上下文变量

    def get_queryset(self):
        return zufang_sh.objects.all()[:10]

@cache_page(60 * 10)
def group_by_city(request, city):
    zufang_list = zufang_sh.objects(city=city)
    total_count= len(zufang_list)
    districts = DM.get(str(city))
    #microdistricts = zufang_sh.objects.item_frequencies("microdistrict").keys()
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
        'districts' : districts

    }

    return render(request, 'Mainapp/index2.html', data)

@cache_page(60 * 10)
def group_by_district(request, district):
    # 获取区县
    # district = request.GET.get('district')
    # 或许该区县的所有数据
    result_list = zufang_sh.objects(district=district)
    total_count = len(result_list)
    # 返回该区县下的商圈
    microdistricts = DM.get(str(district))
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
        # 当前城市的区县
        'microdistricts': microdistricts

        # 当前区县的
    }
    return render(request, 'Mainapp/index2.html', data)

@cache_page(60 * 10)
def group_by_microdistrict(request,microdistrict):
    result_list =  zufang_sh.objects(microdistrict = microdistrict)
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
        'total_count': total_count
    }
    return render(request, 'Mainapp/index2.html', data)



