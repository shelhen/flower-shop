from django.shortcuts import render
from django.views import View
import json, base64, pickle
from django import http
from django.conf import settings
from django_redis import get_redis_connection
from goods.models import Goods
from flower_shop.utils.response_code import RETCODE


class CartsView(View):
    """购物车管理"""

    def post(self, request):
        """保存购物车"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        count = json_dict.get('count')
        selected = json_dict.get('selected', True)  # 可选,如果json_dict存在selectedze返回，否则返回True
        # 校验参数
        # 判断参数是否齐全
        # all()若其中存在元素为空，则返回false
        if not all([sku_id, count]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 校验sku_id是否合法
        try:
            Goods.objects.get(id=sku_id)
        except Goods.DoesNotExist:
            return http.HttpResponseForbidden('参数sku_id错误')
        # 校验count是否是数字
        try:
            count = int(count)
        except Exception as e:
            return http.HttpResponseForbidden('参数count错误')
        # 校验勾选是否是bool
        if selected:
            if not isinstance(selected, bool):
                return http.HttpResponseForbidden('参数selected错误')
        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 如果用户已登录，操作Redis购物车
            redis_conn = get_redis_connection('carts')
            pl = redis_conn.pipeline()

            # 需要以增量计算的形式保存商品数据
            pl.hincrby('carts_%s' % user.id, sku_id, count)
            # 保存商品勾选状态
            if selected:
                pl.sadd('selected_%s' % user.id, sku_id)
            pl.execute()  # 执行
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})  # 响应结果
        else:
            # 如果用户未登录，操作cookie购物车
            # 获取cookie中的购物车数据，并且判断是否有购物车数据
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                # 将 cart_str转成bytes类型的字符串
                cart_str_bytes = cart_str.encode()
                # 将cart_str_bytes转成bytes类型的字典
                cart_dict_bytes = base64.b64decode(cart_str_bytes)
                # 将cart_dict_bytes转成真正的字典
                cart_dict = pickle.loads(cart_dict_bytes)
            else:
                cart_dict = {}
            # 判断当前要添加的商品在cart_dict中是否存在
            if sku_id in cart_dict:
                # 购物车已存在，增量计算
                origin_count = cart_dict[sku_id]['count']
                count += origin_count
            cart_dict[sku_id] = {
                'count': count,
                'selected': selected,
            }
            # 将cart_dict转成bytes类型的字典
            cart_dict_bytes = pickle.dumps(cart_dict)
            # 将cart_dict_bytes转成bytes类型的字符串
            cart_str_bytes = base64.b64encode(cart_dict_bytes)
            # 将cart_str_bytes转成字符串
            cookie_cart_str = cart_str_bytes.decode()

            # 将新的购物车数据写入到cookie
            response = http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})
            response.set_cookie('carts', cookie_cart_str,max_age=60 * 60 * 24 * 7)
            # 响应结果
            return response

    def get(self, request):
        """查询购物车"""
        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，查询redis购物车
            # 创建链接到redis的对象
            redis_conn = get_redis_connection('carts')
            # 查询hash数据 # {b'9012481': b'1', b'9012243': b'2'} 一个购买一个，另一个购买两个
            redis_cart = redis_conn.hgetall('carts_%s' % user.id)
            # 查询selected 数据 {b'9012243', b'9012481'} 两个ture
            redis_selected = redis_conn.smembers('selected_%s' % user.id)
            """
            {
                "sku_id1":{
                    "count":"1",
                    "selected":"True",
                    "delivery":"0"
                },
                "sku_id2":{
                    "count":"2",
                    "selected":"True",
                    "delivery":"1"
                },
            }
            """
            cart_dict = {}
            # 将redis_cart和redis_selected进行数据结构的构造，合并数据，数据结构跟未登录用户购物车结构一致
            for sku_id, count in redis_cart.items():
                cart_dict[int(sku_id)] = {
                    "count": int(count),
                    "selected": sku_id in redis_selected
                }
        else:
            # 用户未登录，查询cookies购物车
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                # 将 cart_str转成bytes类型的字符串
                cart_str_bytes = cart_str.encode()
                # 将cart_str_bytes转成bytes类型的字典
                cart_dict_bytes = base64.b64decode(cart_str_bytes)
                # 将cart_dict_bytes转成真正的字典
                cart_dict = pickle.loads(cart_dict_bytes)
            else:
                cart_dict = {}
        # {9012481: {'count': 1, 'delivery': 0, 'selected': True}, 9012510: {'count': 3, 'delivery': 1, 'selected': True}, 9012504: {'count': 2, 'delivery': 1, 'selected': True}}
        # 构造响应数据
        # 获取字典中所有的key,(sku_id)
        sku_ids = cart_dict.keys()
        # 一次性查询出所有的skus
        skus = Goods.objects.filter(id__in=sku_ids)
        cart_skus = []
        for sku in skus:
            cart_skus.append({
                'id': sku.id,
                'count': cart_dict.get(sku.id).get('count'), # 一个sku的总数目
                'selected': str(cart_dict.get(sku.id).get('selected')),  # 将True，转'True'，方便json解析
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': str(sku.price),  # 从Decimal('10.2')中取出'10.2'，方便json解析
                'mprice':str(sku.market_price* cart_dict.get(sku.id).get('count')),
                'amount': str(sku.price * cart_dict.get(sku.id).get('count'))
            })

        context = {
            'cart_skus': cart_skus,
        }  #
        # 渲染购物车页面
        return render(request, 'cart.html', context)

    def put(self, request):
        """修改购物车"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        count = json_dict.get('count')
        selected = json_dict.get('selected', True)

        # 判断参数是否齐全
        if not all([sku_id, count]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断sku_id是否存在
        try:
            sku = Goods.objects.get(id=sku_id)
        except Goods.DoesNotExist:
            return http.HttpResponseForbidden('商品sku_id不存在')
        # 判断count是否为数字
        try:
            count = int(count)
        except Exception:
            return http.HttpResponseForbidden('参数count有误')
        # 判断selected是否为bool值
        if selected:
            if not isinstance(selected, bool):
                return http.HttpResponseForbidden('参数selected有误')

        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，修改redis购物车
            redis_conn = get_redis_connection('carts')
            pl = redis_conn.pipeline()

            # 由于后端收到的数据是最终的结果，所以"覆盖写入"
            # redis_conn.hincrby() # 使用新值加上旧值（增量）
            pl.hset('carts_%s' % user.id, sku_id, count)
            # 修改勾选状态
            if selected:
                pl.sadd('selected_%s' % user.id, sku_id)
            else:
                pl.srem('selected_%s' % user.id, sku_id)
            # 执行
            pl.execute()

            # 创建响应对象
            cart_sku = {
                'id': sku_id,
                'count': count,
                'selected': selected,
                'name': sku.name,
                'price': sku.price,
                'mprice': sku.market_price * count,
                'amount': sku.price * count,
                'default_image_url': sku.default_image.url
            }
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '修改购物车成功', 'cart_sku': cart_sku})
        else:
            # 用户未登录，修改cookie购物车
            # 获取cookie中的购物车数据，并且判断是否有购物车数据
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                # 将 cart_str转成bytes类型的字符串
                cart_str_bytes = cart_str.encode()
                # 将cart_str_bytes转成bytes类型的字典
                cart_dict_bytes = base64.b64decode(cart_str_bytes)
                # 将cart_dict_bytes转成真正的字典
                cart_dict = pickle.loads(cart_dict_bytes)
            else:
                cart_dict = {}

            # 由于后端收到的是最终的结果，所以"覆盖写入"
            cart_dict[sku_id] = {
                'count': count,
                'selected': selected
            }

            # 创建响应对象
            cart_sku = {
                'id': sku_id,
                'count': count,
                'selected': selected,
                'name': sku.name,
                'price': sku.price,
                'mprice': sku.market_price * count,
                'amount': sku.price * count,
                'default_image_url': sku.default_image.url
            }

            # 将cart_dict转成bytes类型的字典
            cart_dict_bytes = pickle.dumps(cart_dict)
            # 将cart_dict_bytes转成bytes类型的字符串
            cart_str_bytes = base64.b64encode(cart_dict_bytes)
            # 将cart_str_bytes转成字符串
            cookie_cart_str = cart_str_bytes.decode()

            # 将新的购物车数据写入到cookie
            response = http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'cart_sku': cart_sku})
            response.set_cookie('carts', cookie_cart_str)

            # 响应结果
            return response

    def delete(self, request):
        """删除购物车"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')

        # 判断sku_id是否存在
        try:
            Goods.objects.get(id=sku_id)
        except Goods.DoesNotExist:
            return http.HttpResponseForbidden('商品不存在')

        # 判断用户是否登录
        user = request.user
        if user is not None and user.is_authenticated:
            # 用户已登录，删除redis购物车
            redis_conn = get_redis_connection('carts')
            pl = redis_conn.pipeline()

            # 删除hash购物车商品记录
            pl.hdel('carts_%s' % user.id, sku_id)
            # 同步移除勾选状态
            pl.srem('selected_%s' % user.id, sku_id)
            pl.execute()

            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})
        else:
            # 用户未登录，删除cookie购物车
            # 获取cookie中的购物车数据，并且判断是否有购物车数据
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                # 将 cart_str转成bytes类型的字符串
                cart_str_bytes = cart_str.encode()
                # 将cart_str_bytes转成bytes类型的字典
                cart_dict_bytes = base64.b64decode(cart_str_bytes)
                # 将cart_dict_bytes转成真正的字典
                cart_dict = pickle.loads(cart_dict_bytes)
            else:
                cart_dict = {}

            # 构造响应对象
            response = http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})

            # 删除字典指定key所对应的记录
            if sku_id in cart_dict:
                del cart_dict[sku_id] # 如果删除的key不存在，会抛出异常

                # 将cart_dict转成bytes类型的字典
                cart_dict_bytes = pickle.dumps(cart_dict)
                # 将cart_dict_bytes转成bytes类型的字符串
                cart_str_bytes = base64.b64encode(cart_dict_bytes)
                # 将cart_str_bytes转成字符串
                cookie_cart_str = cart_str_bytes.decode()

                # 写入新的cookie
                response.set_cookie('carts', cookie_cart_str)

            return response


class CartsSimpleView(View):
    """商品页面右上角购物车"""

    def get(self, request):
        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，查询Redis购物车
            redis_conn = get_redis_connection('carts')
            redis_cart = redis_conn.hgetall('carts_%s' % user.id)
            cart_selected = redis_conn.smembers('selected_%s' % user.id)
            # 将redis中的两个数据统一格式，跟cookie中的格式一致，方便统一查询
            cart_dict = {}
            for sku_id, count in redis_cart.items():
                cart_dict[int(sku_id)] = {
                    'count': int(count),
                    'selected': sku_id in cart_selected
                }
        else:
            # 用户未登录，查询cookie购物车
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict = {}
        sku_ids = cart_dict.keys()
        skus = Goods.objects.filter(id__in=sku_ids)
        amounts = [cart_dict.get(sku.id).get('count') for sku in skus]
        cart_total_count=0
        for i in amounts:
            cart_total_count+=int(i)
        # 响应json列表数据
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'cart_total_count': cart_total_count})


class CartsSelectAllView(View):
    """全选购物车"""

    def put(self, request):
        # 接收参数
        json_dict = json.loads(request.body.decode())
        selected = json_dict.get('selected', True)

        # 校验参数
        if selected:
            if not isinstance(selected, bool):
                return http.HttpResponseForbidden('参数selected有误')

        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，操作redis购物车
            redis_conn = get_redis_connection('carts')

            # 获取所有的记录 {b'3': b'1', b'5': b'2'}
            redis_cart = redis_conn.hgetall('carts_%s' % user.id)
            # 获取字典中所有的key [b'3', b'5']
            redis_sku_ids =  redis_cart.keys()
            # 判断用户是否全选
            if selected:
                # 全选
                redis_conn.sadd('selected_%s' % user.id, *redis_sku_ids)
            else:
                # 取消全选
                redis_conn.srem('selected_%s' % user.id, *redis_sku_ids)

            # 响应结果
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})
        else:
            # 用户未登录，操作cookie购物车
            # 获取cookie中的购物车数据，并且判断是否有购物车数据
            cart_str = request.COOKIES.get('carts')

            # 构造响应对象
            response = http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})

            if cart_str:
                # 将 cart_str转成bytes类型的字符串
                cart_str_bytes = cart_str.encode()
                # 将cart_str_bytes转成bytes类型的字典
                cart_dict_bytes = base64.b64decode(cart_str_bytes)
                # 将cart_dict_bytes转成真正的字典
                cart_dict = pickle.loads(cart_dict_bytes)

                # 遍历所有的购物车记录
                for sku_id in cart_dict:
                    cart_dict[sku_id]['selected'] = selected # True / False

                # 将cart_dict转成bytes类型的字典
                cart_dict_bytes = pickle.dumps(cart_dict)
                # 将cart_dict_bytes转成bytes类型的字符串
                cart_str_bytes = base64.b64encode(cart_dict_bytes)
                # 将cart_str_bytes转成字符串
                cookie_cart_str = cart_str_bytes.decode()

                # 重写将购物车数据写入到cookie
                response.set_cookie('carts', cookie_cart_str)

            return response

