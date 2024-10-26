from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from flower_shop.utils.views import LoginRequiredMixin, LoginRequiredJSONMixin
from django.views import View
from django_redis import get_redis_connection
from decimal import Decimal
import json
from django import http
from django.utils import timezone
from django.db import transaction
from django.conf import settings
from users.models import Address
from goods.models import Goods
from .models import OrderInfo, OrderGoods
from flower_shop.utils.response_code import RETCODE


# Create your views here.
class OrderSettlementView(LoginRequiredMixin, View):
    """结算订单"""
    def get(self, request):
        """查询并展示要结算的订单数据"""
        user = request.user  # 获取登录用户
        try:  # 查询用户收货地址:查询登录用户的没有被删除的收货地址
            addresses = Address.objects.filter(user=user, is_deleted=False)
        except Exception as e:  # 如果没有查询出地址，可以去编辑收货地址
            addresses = None  # 查询redis购物车中被勾选的商品
        redis_conn = get_redis_connection('carts')  # 所有的购物车数据，包含了勾选和未勾选 ：{b'1': b'1', b'2': b'2'}
        redis_cart = redis_conn.hgetall('carts_%s' % user.id)  # 被勾选的商品的sku_id：[b'1']
        redis_selected = redis_conn.smembers('selected_%s' % user.id)
        new_cart_dict = {}  # 构造redis购物车中被勾选的商品的数据 {b'1': b'1'}
        for sku_id in redis_selected:
            new_cart_dict[int(sku_id)] = int(redis_cart[sku_id])
        category = []  # 获取被勾选的商品的sku_id
        sku_ids = new_cart_dict.keys()
        skus = Goods.objects.filter(id__in=sku_ids)
        total_count = 0
        total_amount = Decimal(0.00)
        for sku in skus:
            category.append(sku.category_id)
            # 遍历skus给每个sku补充count（数量）和amount（小计）
            sku.count = new_cart_dict[sku.id]
            sku.amount = sku.price * sku.count  # Decimal类型的
            # 累加数量和金额
            total_count += sku.count
            total_amount += sku.amount  # 类型不同不能运算   # 取出所有的sku
        goods = Goods.objects.filter(category_id__in=category).order_by('desc_detail')  # 查询到当前购买的鲜花种类下的所有鲜花花语数据
        desc = set([good.desc_detail for good in goods])  # 查询获取所有花语数据
        try:
            desc = list(desc)[:7]
        except:
            print('花语数据不足4个')
            desc = list(desc)[:4]
        freight = settings.FREIGHT
        context = {
            'addresses': addresses,
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount,
            'freight': freight,
            'payment_amount': total_amount,
            'desc': desc
        }
        return render(request, 'order.html', context)


class OrderCommitView(LoginRequiredJSONMixin, View):
    """提交订单"""
    def post(self, request):
        """保存订单基本信息和订单商品信息"""
        json_dict = json.loads(request.body.decode())  # 接收参数
        address_id = json_dict.get('address_id')
        pay_method = json_dict.get('pay_method')
        delivery = json_dict.get('delivery')
        words = json_dict.get('words')
        if not all([address_id, pay_method, delivery]):
            return http.HttpResponseForbidden('缺少必传参数')
        try:  # 判断address_id是否合法
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return http.HttpResponseForbidden('参数address_id错误')
        if pay_method not in [OrderInfo.PAY_METHODS_ENUM['CASH'], OrderInfo.PAY_METHODS_ENUM['ALIPAY']]:
            return http.HttpResponseForbidden('参数pay_method错误')
        if delivery not in (1, 2):
            return http.HttpResponseForbidden('参数delivery错误')
        with transaction.atomic():  # 开启一次事务
            save_id = transaction.savepoint()  # 在数据库操作之前需要指定保存点（保存数据库最初的状态）
            try:  # 暴力回滚
                if pay_method==OrderInfo.PAY_METHODS_ENUM['ALIPAY']:
                    status = OrderInfo.ORDER_STATUS_ENUM['UNPAID']  # 如果为支付宝支付，状态改为待支付
                elif pay_method == OrderInfo.PAY_METHODS_ENUM['CASH']:
                    status = OrderInfo.ORDER_STATUS_ENUM['UNSEND']  # 如果为现金支付，状态改为待发货
                else:
                    status = OrderInfo.ORDER_STATUS_ENUM['UNRECEIVED']  # 其他暂时均改为 待收货
                user = request.user  # 获取登录用户
                order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%04d' % user.id) # 获取订单编号：时间+user_id == '20190526165742000000001'
                # 保存订单基本信息（一）
                order = OrderInfo.objects.create( order_id=order_id,user=user,address=address,total_count=0,total_amount=Decimal(0.00),freight=Decimal(settings.FREIGHT*(delivery-1)),pay_method=pay_method,words=words,status=status)
                # 保存订单商品信息（多）
                redis_conn = get_redis_connection('carts')  # 查询redis购物车中被勾选的商品
                redis_cart = redis_conn.hgetall('carts_%s' % user.id)  # 所有的购物车数据，包含了勾选和未勾选 ：{b'1': b'1', b'2': b'2'}
                redis_selected = redis_conn.smembers('selected_%s' % user.id)  # 被勾选的商品的sku_id：[b'1']
                new_cart_dict = {}  # 构造购物车中被勾选的商品的数据 {b'1': b'1'}
                for sku_id in redis_selected:
                    new_cart_dict[int(sku_id)] = int(redis_cart[sku_id])
                sku_ids = new_cart_dict.keys()  # 获取被勾选的商品的sku_id
                for sku_id in sku_ids:
                    while True:  # 每个商品都有多次下单的机会，直到库存不足
                        sku = Goods.objects.get(id=sku_id)  # 读取购物车商品信息 # 查询商品和库存信息时，不能出现缓存，所以没用filter(id__in=sku_ids)
                        origin_stock = sku.stock  # 获取原始的库存和销量
                        origin_sales = sku.sales
                        sku_count = new_cart_dict[sku.id]  # 获取要提交订单的商品的数量
                        if sku_count > origin_stock:  # 判断商品数量是否大于库存，如果大于，响应"库存不足"
                            transaction.savepoint_rollback(save_id)  # 库存不足，回滚
                            return http.JsonResponse({'code': RETCODE.STOCKERR, 'errmsg': '库存不足'})
                        new_stock = origin_stock - sku_count  # 模拟网络延迟
                        new_sales = origin_sales + sku_count
                        result = Goods.objects.filter(id=sku_id, stock=origin_stock).update(stock=new_stock, sales=new_sales)
                        if result == 0:  # 如果在更新数据时，原始数据变化了，返回0；表示有资源抢夺
                            # 库存 10，要买1，但是在下单时，有资源抢夺，被买走1，剩下9个，如果库存依然满足，继续下单，直到库存不足为止
                            # return http.JsonResponse('下单失败')
                            continue
                        sku.sales += sku_count
                        sku.save()
                        OrderGoods.objects.create( order=order, sku=sku, count=sku_count, price=sku.price)
                        order.total_count += sku_count  # 累加订单商品的数量和总价到订单基本信息表
                        order.total_amount += sku_count * sku.price
                        break  # 下单成功，退出循环break
                order.total_amount += order.freight  # 再加最后的运费
                order.save()
                for sku_id in sku_ids:  # 保存成功后，清空redis数据库
                    pl = redis_conn.pipeline()
                    pl.hdel('carts_%s' % user.id, sku_id)  # 删除hash购物车商品记录
                    pl.srem('selected_%s' % user.id, sku_id)  # 同步移除勾选状态
                    pl.execute()
            except Exception as e:
                transaction.savepoint_rollback(save_id)
                return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '下单失败'})
            # 数据库操作成功，明显提交一次事务
            transaction.savepoint_commit(save_id)
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'order_id': order_id})


class CommentView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.GET.get('order_id')  # 接收订单编号
        try:  # 查询订单商品列表
            order = OrderInfo.objects.get(pk=order_id, user_id=request.user.id)
        except:
            return http.Http404('商品编号无效')
        skus = []  # 获取订单的所有商品
        for detail in order.skus.filter(is_commented=False):  # detail表示OrderGoods类型的对象
            skus.append({
                'sku_id': detail.sku.id,
                'default_image_url': detail.sku.default_image.url,
                'name': detail.sku.name,
                'price': str(detail.price),
                'order_id': order_id
            })
        context = { 'skus': skus}
        return render(request, 'judge.html', context)
    def post(self, request):
        data = json.loads(request.body.decode())
        order_id = data.get('order_id')
        sku_id = data.get('sku_id')
        comment = data.get('comment')
        score = data.get('score')
        is_anonymous = data.get('is_anonymous')
        if not all([order_id, sku_id, comment, score]):
            return http.JsonResponse({ 'code': RETCODE.PARAMERR, 'errmsg': '参数不完整'})
        if not isinstance(is_anonymous, bool):
            return http.JsonResponse({ 'code': RETCODE.PARAMERR, 'errmsg': '是否匿名参数错误' })
        order_goods = OrderGoods.objects.get(order_id=order_id, sku_id=sku_id)  # 查询OrderGoods对象
        order_goods.comment = comment
        order_goods.score = int(score)
        order_goods.is_anonymous = is_anonymous
        order_goods.is_commented = True
        order_goods.save()
        OrderInfo.objects.filter(order_id=order_id, status=OrderInfo.ORDER_STATUS_ENUM['UNCOMMENT']).update(
            status=OrderInfo.ORDER_STATUS_ENUM["FINISHED"])
        Goods.objects.filter(id=sku_id).update(comments=order_goods.sku.comments + 1)  # 评论完毕后，评论量加一
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})


class CommentSKUView(View):
    def get(self, request, sku_id):
        comments = OrderGoods.objects.filter(sku_id=sku_id, is_commented=True) # 查询指定sku_id的所有评论信息
        comment_list = []
        for detail in comments:  # detail表示OrderGoods对象
            username = detail.order.user.username
            username = '******' if detail.is_anonymous else username[0] + '****' + username[1]
            comment_list.append({ 'username': username, 'comment': detail.comment, 'score': detail.score })
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': "OK", 'goods_comment_list': comment_list})
class OrderConfirmView(LoginRequiredMixin, View):
    def put(self, request, order_id):
        user = request.user
        if not order_id:
            return http.HttpResponseForbidden('缺少必传参数')
        try:
            OrderInfo.objects.get(order_id=order_id, user=user, status=OrderInfo.ORDER_STATUS_ENUM['UNRECEIVED'])
        except OrderInfo.DoesNotExist:
            return http.HttpResponseForbidden('订单信息错误')
        OrderInfo.objects.filter(order_id=order_id, status=OrderInfo.ORDER_STATUS_ENUM['UNRECEIVED']).update(
            status=OrderInfo.ORDER_STATUS_ENUM["UNCOMMENT"])   # 修改订单状态由"待支付"修改为"代发货"
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '确认收货成功'})
class OrderSendView(View):
    def put(self, request, order_id, status):
        if not all([order_id, status]):
            return http.JsonResponse({'code': RETCODE.PARAMERR, 'errmsg': '参数不完整'})
        try:
            OrderInfo.objects.get(order_id=order_id, status=status)
        except OrderInfo.DoesNotExist:
            return http.HttpResponseForbidden('订单信息错误')
        if int(status)==OrderInfo.ORDER_STATUS_ENUM['UNSEND']:
            OrderInfo.objects.filter(order_id=order_id, status=OrderInfo.ORDER_STATUS_ENUM['UNSEND']).update(
                status=OrderInfo.ORDER_STATUS_ENUM["UNRECEIVED"])
            errmsg = '发货成功'
        elif int(status)==OrderInfo.ORDER_STATUS_ENUM['DRAWBACK'] :
            OrderInfo.objects.filter(order_id=order_id, status=OrderInfo.ORDER_STATUS_ENUM['DRAWBACK']).update(
                status=OrderInfo.ORDER_STATUS_ENUM["UNFINISHED"])
            errmsg = '退款成功'
        else:
            return http.HttpResponseForbidden('订单信息错误')
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': errmsg})
class UserCommentView(LoginRequiredMixin, View):
    def get(self, request, page_num):
        user = request.user
        orderids=[]
        orders = OrderInfo.objects.filter(user=user, status=OrderInfo.ORDER_STATUS_ENUM['FINISHED'])
        for order in orders:
            orderids.append(order.order_id)
        commentgoods = OrderGoods.objects.filter(order_id__in=orderids,is_commented=True).order_by("-create_time")
        for good in commentgoods:
            good.img = good.sku.default_image
            good.name = good.sku.name.replace(' ', '')
            if good.score==1:
                good.score='stars_one'
            elif good.score==2:
                good.score = 'stars_two'
            elif good.score == 3:
                good.score = 'stars_three'
            elif good.score == 4:
                good.score = 'stars_four'
            else:
                good.score = 'stars_five'
            good.time=str(good.update_time)[:-13]
        paginator = Paginator(commentgoods, 3)
        page_orders = paginator.page(page_num)
        total_page = paginator.num_pages
        context = {
            'goods_comment_list': page_orders,
            'total_page': total_page,
            'page_num':  int(page_num),
        }
        return render(request, 'user_center_judge.html', context)
class DrawbackView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.GET.get('order_id')
        try:
            order = OrderInfo.objects.get(order_id=order_id, user_id=request.user.id)
        except:
            return http.Http404('商品编号无效')
        total_amount = Decimal(0.00)
        skus = []
        for sku in order.skus.filter():
            skus.append({
                'sku_id': sku.sku.id,
                'default_image_url': sku.sku.default_image.url,
                'name': sku.sku.name,
                'count':sku.count,
                'price': str(sku.price),
                'amount':sku.price * sku.count  # Decimal类型的
            })
            total_amount+=sku.price * sku.count
        context = {
            'skus': skus,
            'total_amount':total_amount,
            'order_id':order_id
        }
        return render(request, 'withdraw.html', context)
    def post(self, request):
        data = json.loads(request.body.decode())
        order_id = data.get('order_id')
        total_amount=data.get('total_amount')
        describe = data.get('describe')
        is_anonymous = data.get('is_anonymous')
        if not all([order_id, total_amount]):
            return http.JsonResponse({
                'code': RETCODE.PARAMERR,
                'errmsg': '参数不完整'
            })
        if not isinstance(is_anonymous, bool):
            return http.JsonResponse({
                'code': RETCODE.PARAMERR,
                'errmsg': '是否匿名参数错误'
            })
        OrderInfo.objects.filter(order_id=order_id).update(status=OrderInfo.ORDER_STATUS_ENUM["DRAWBACK"])
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '申请退款成功，请耐心等待。'})