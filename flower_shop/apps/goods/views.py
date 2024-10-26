from django.shortcuts import render
from django.views import View
from django import http
from django.conf import settings
# 分页器（有100万文字，需要制作成为一本书，先规定每页多少文字，然后得出一共多少页）
# 数据库中的记录就是文字，我们需要考虑在分页时每页记录的条数，然后得出一共多少页
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone  # 处理时间的工具
from datetime import datetime
from .models import GoodsCategory, Goods, GoodImage, DetialImage, GoodsVisitCount
from flower_shop.utils.response_code import RETCODE
# Create your views here.


class ListView(View):
    """商品列表页"""
    def get(self, request, category_id, page_num):
        """查询并渲染商品列表页"""
        sort = request.GET.get('sort', 'default')
        # 根据sort选择排序字段，排序字段必须是模型类的属性
        sort_field = 'price' if sort == 'price' else ('-sales' if sort == 'hot' else 'create_time')
        sort = "default" if sort not in ['price', 'hot'] else sort  # 获取sort(排序规则): 如果sort没有值，取'default'
        categories = GoodsCategory.objects.all()  # 查询所有类别
        try:
            if not int(category_id):
                goods = Goods.objects.filter(is_launched=True).order_by(sort_field)  # 若ID=0则说明查询得到所有商品信息
            else:  # 若id不为0，为1-8之间的数字，则查询得到特定分类下商品信息
                goods = Goods.objects.filter(category_id=category_id, is_launched=True).order_by(sort_field)
        except GoodsCategory.DoesNotExist:
            return http.HttpResponseForbidden('参数category_id不存在')
        paginator = Paginator(goods, 8)  # 创建分页器  # 把goods进行分页，每页8条记录
        try:
            page_skus = paginator.page(page_num)  # 获取到page_num页中的8条记录
        except EmptyPage:
            return http.HttpResponseNotFound('Empty Page')
        total_page = paginator.num_pages  # 获取总页数：前端的分页插件需要使用
        context = {
            'category_id': int(category_id),
            'categories': categories,
            'page_skus': page_skus,
            'page_num': page_num,
            'total_page': total_page,
            'sort': sort,
        }  # 构造上下文
        return render(request, 'list.html', context)


class HotGoodsView(View):
    """热销排行"""
    def get(self, request):
        # 查询指定分类的SKU信息，而且必须是上架的状态，然后按照销量由高到低排序，最后切片取出前两位
        goods = Goods.objects.filter(is_launched=True).order_by('-sales')[:3]
        # 将模型列表转字典列表，构造JSON数据
        hot_skus = []
        for sku in goods:
            sku_dict = {
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url # 记得要取出全路径
            }
            hot_skus.append(sku_dict)
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'hot_skus': hot_skus})
class DetailView(View):
    """商品详情页"""
    def get(self, request, sku_id):
        """提供商品详情页"""
        try:
            good = Goods.objects.filter(id=sku_id)[0]
            imgs = GoodImage.objects.filter(good_id=sku_id)
            images = DetialImage.objects.filter(good_id=sku_id)
            img_list = [img.image.name for img in imgs]
            img_list.append(good.default_image.name)
        except:
            return render(request, '404.html')
        # 构造上下文
        context = {
            'good': good,
            'freight': str(settings.FREIGHT),
            'imgs': img_list,
            'images': images
        }
        return render(request, 'detail.html', context)


class DetailVisitView(View):
    """统计分类商品的访问量"""
    def post(self, request, category_id):
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return http.HttpResponseForbidden('category_id 不存在')
        t = timezone.localtime()  # 获取当天的日期
        today_str = '%d-%02d-%02d' % (t.year, t.month, t.day)  # 获取当天的时间字符串
        # 将当天的时间字符串转成时间对象datetime，为了跟date字段的类型匹配 2019:05:23  2019-05-23
        today_date = datetime.strptime(today_str, '%Y-%m-%d')  # 时间字符串转时间对象；datetime.strftime() # 时间对象转时间字符串
        try: # 判断当天中指定的分类商品对应的记录是否存在
            counts_data = GoodsVisitCount.objects.get(date=today_date, category=category)   # 如果存在，直接获取到记录对应的对象
        except GoodsVisitCount.DoesNotExist:
            counts_data = GoodsVisitCount()   # 如果不存在，直接创建记录对应的对象
        try:
            counts_data.category = category
            counts_data.count += 1
            counts_data.date = today_date
            counts_data.save()
        except Exception as e:
            return http.HttpResponseServerError('统计失败')
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})  # 响应结果
