from django.shortcuts import render
from django.views import View
from contents.models import Slide, Content, ContentImage
from goods.models import Goods
from django.core.paginator import Paginator, EmptyPage
from django import http
import random
from django.utils.timezone import make_aware
import datetime
from orders.models import OrderInfo
from flower_shop.utils.response_code import RETCODE
from contents.utils import get_dashboard_data, get_deals, get_sales


class IndexView(View):
    """提供首页轮播图"""
    def get(self, request):
        # 查询所有轮播图
        slides = Slide.objects.all()
        # 查询指定分类的SKU信息，而且必须是上架的状态，然后按照销量由高到低排序，最后切片取出前八位
        goods = Goods.objects.filter(is_launched=True, category=1).order_by('-sales')
        random_nums=random.sample(range(0,len(goods) - 1), 5)
        offers = [goods[i] for i in random_nums]
        # \static\imgs\functions\banner_01.png
        context = {
            'slides': slides,
            'hot_goods': goods[:4],
            'hot_goods2': goods[4:6],
            'offers': offers[1:5],
            'main_offer': offers[0]
        }
        return render(request, 'index.html', context=context)


class FloweryListView(View):
    """花语列表页"""
    def get(self, request, page_num):
        """查询并渲染花语列表页"""
        contents = Content.objects.all().order_by('create_time')
        for content in contents:
            content.time = str(content.create_time)[:-6]
            content.text = content.intro + content.text
        paginator = Paginator(contents, 6)
        try:
            page_contents = paginator.page(page_num)  # 获取到page_num页中的8条记录
        except EmptyPage:
            return http.HttpResponseNotFound('Empty Page')
        # 获取总页数：前端的分页插件需要使用
        total_page = paginator.num_pages
        # 构造上下文
        context = {
            'page_contents': page_contents,
            'page_num': page_num,
            'total_page': total_page,
        }
        return render(request, 'flowerylist.html', context)


class FloweryView(View):

    def get(self, request, content_id):
        """查询并渲染花语详情页"""
        try:
            content = Content.objects.filter(id=content_id)[0]
            imgs = ContentImage.objects.filter(content_id=content_id)
        except Content.DoesNotExist:
            return http.HttpResponseNotFound('content_id 不存在')
        Content.objects.filter(id=content.id).update(count=content.count+1)
        content.time = str(content.create_time)[:-6]
        context = {
            'content': content,
            "imgs": imgs
        }
        return render(request, 'flowery.html', context)


class HotFloweryView(View):
    """花语浏览量排行"""

    def get(self, request):

        contents = Content.objects.all().order_by('-count')[:6]
        # 将模型列表转字典列表，构造JSON数据
        hot_contents = []
        for content in contents:
            content_dict = {
                'id': content.id,
                'title': content.title,
                'image': content.image.name,
                'count': content.count,
            }
            hot_contents.append(content_dict)

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'hot_contents': hot_contents})


class DashBoardView(View):

    def get(self, request, page_num):
        now_date = make_aware(datetime.datetime.now())
        start_date = now_date.date() - datetime.timedelta(1)
        orders = OrderInfo.objects.filter(create_time__gte=start_date,create_time__lt=now_date, status=6)
        finishs = [[order.order_id, str(order.update_time)[:-13], order.total_amount] for order in orders]
        finishs=finishs[5] if len(finishs)>5 else finishs
        paginator = Paginator(get_deals(), 9)
        try:
            page_deals = paginator.page(page_num)  # 获取到page_num页中的9条记录
        except EmptyPage:
            return http.HttpResponseNotFound('Empty Page')
        # 获取总页数：前端的分页插件需要使用
        total_page = paginator.num_pages
        context = {
            'dashboard': get_dashboard_data(),
            'finishs': finishs,
            "page_deals": page_deals,
            "page_num": page_num,
            "total_page": total_page,
            'counts':get_sales()[0],
            'dates':get_sales()[1],
        }
        return render(request, 'dashaboard.html', context=context)