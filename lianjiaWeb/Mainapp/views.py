from django.shortcuts import render
from django.views import generic
from .models import zufang_sh
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pypinyin import pinyin

from django.core.cache import cache #引入缓存模块

# Create your views here.

# 用于获取数据库中model的列表
class IndexView(generic.ListView):
    template_name = "Mainapp/test.html"      # 需要渲染的模板
    context_object_name = "houses"           # 模板中使用的上下文变量

    def get_queryset(self):
        return zufang_sh.objects.all()[:10]


def listing(request):
    zufang_list = zufang_sh.objects.all()
    total_count= len(zufang_list)
    districts = zufang_sh.objects.item_frequencies("district").keys()
    microdistricts = zufang_sh.objects.item_frequencies("microdistrict").keys()
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
        'microdistricts': microdistricts,
        'districts' : districts

        # 当前区县的
    }
    cache.set('key', 'value', 30 * 60)  # 写入key为key，值为value的缓存，有效期30分钟
    cache.has_key('key')  # 判断key为k是否存在
    cache.get('key')  # 获取key为k的缓存
    return render(request, 'Mainapp/index2.html', data)



# 按区县分组 请求参数中包含 1. 区域 2. 方式 3.租金 4 户型 5. 朝向 6. 排序方式
def group_by_district(request,district):
    # 获取区县
    # district = request.GET.get('district')
    # 或许该区县的所有数据
    result_list = zufang_sh.objects(district=district)
    total_count = len(result_list)
    # 返回该区县下的商圈
    microdistricts = result_list.item_frequencies("microdistrict").keys()
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



