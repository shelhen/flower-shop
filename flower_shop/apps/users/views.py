from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django import http
import re, json
from django.contrib.auth import login, logout, authenticate
from django_redis import get_redis_connection
from django.db import DatabaseError
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User, Address
from flower_shop.utils.response_code import RETCODE
from flower_shop.utils.views import LoginRequiredJSONMixin
from goods.models import Goods
from orders.models import OrderInfo, OrderGoods
from carts.utils import merge_carts_cookies_redis


# 用户地址上限
USER_ADDRESS_COUNTS_LIMIT = 8

class RegisterView(View):
    """用户注册"""

    def get(self, request):
        """提供用户注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        """实现用户注册业务逻辑"""
        # 接收参数：表单参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        sms_code_client = request.POST.get('sms_code')
        allow = request.POST.get('allow')
        # 校验参数：前后端的校验需要分开，避免恶意用户越过前端逻辑发请求，要保证后端的安全，前后端的校验逻辑相同
        # 判断参数是否齐全:all([列表])：会去校验列表中的元素是否为空，只要有一个为空，返回false
        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        # 判断短信验证码是否输入正确
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None:
            return render(request, 'register.html', {'sms_code_errmsg': '短信验证码已失效'})
        if sms_code_client != sms_code_server.decode():
            return render(request, 'register.html', {'sms_code_errmsg': '输入短信验证码有误'})
        # 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')
        # 保存注册数据：是注册业务的核心
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg':'注册失败'})
        # 实现状态保持
        login(request, user)
        # 响应结果:重定向到首页
        response = redirect(reverse('contents:index'))
        # 为了实现在首页的右上角展示用户名信息，我们需要将用户名缓存到cookie中
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        # 响应结果:重定向到首页
        return response


class MobileCountView(View):
    """判断手机号是否重复注册"""

    def get(self, request, mobile):
        """
        :param mobile: 手机号
        :return: JSON
        """
        count = User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})


class UsernameCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        """
        :param username: 用户名
        :return: JSON
        """
        # 实现主体业务逻辑：使用username查询对应的记录的条数(filter返回的是满足条件的结果集)
        count = User.objects.filter(username=username).count()
        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})


class LoginView(View):
    """用户登录"""

    def get(self, request):
        """提供用户登录页面"""
        return render(request, 'login.html')

    def post(self, request):
        """实现用户登录逻辑"""

        # 接收参数
        mobile = request.POST.get('mobile')
        sms_code_client = request.POST.get('sms_code')
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')
        # 判断登陆方式
        if username!=None:
            if not all([username, password]):
                return http.HttpResponseForbidden('缺少必传参数')
            if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
                return http.HttpResponseForbidden('请输入正确的用户名或手机号')
            if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
                return http.HttpResponseForbidden('密码最少8位，最长20位')
            # 认证用户:使用账号查询用户是否存在，如果用户存在，再校验密码是否正确
            user = authenticate(username=username, password=password)
            if user is None:
                return render(request, 'login.html', {'account_errmsg': '账号或密码错误'})
        elif mobile!=None:
            # 手机号后端验证
            if not re.match(r'^1[3-9]\d{9}$', mobile):
                return http.HttpResponseForbidden('请输入正确的手机号码')
            # 判断短信验证码是否输入正确
            redis_conn = get_redis_connection('verify_code')
            sms_code_server = redis_conn.get('sms_%s' % mobile)
            if sms_code_server is None:
                return render(request, 'login.html', {'sms_code_errmsg': '短信验证码已失效'})
            if sms_code_client != sms_code_server.decode():
                return render(request, 'login.html', {'sms_code_errmsg': '输入短信验证码有误'})
            # 认证用户:使用账号查询用户手机是否存在，如果手机存在
            user = authenticate(username=mobile)
            remembered='off'
            if user is None:
                return render(request, 'login.html', {'account_errmsg': '手机号不存在'})
        else:
            return render(request, 'login.html', {'account_errmsg': '遇到错误，请重试！'})
        # 状态保持
        login(request, user)
        # 使用remembered确定状态保持周期（实现记住登录）
        if remembered != 'on':
            # 没有记住登录：状态保持在浏览器会话结束后就销毁
            request.session.set_expiry(0) # 单位是秒
        else:
            # 记住登录：状态保持周期为两周:默认是两周
            request.session.set_expiry(None)

        # 响应结果
        # 先取出next
        next = request.GET.get('next')
        if next:
            # 重定向到next
            response = redirect(next)
        else:
            # 重定向到首页
            response = redirect(reverse('contents:index'))
        # 为了实现在首页的右上角展示用户名信息，我们需要将用户名缓存到cookie中
        # response.set_cookie('keys', 'val', 'expiry')
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        # merge_carts_cookies_redis
        response = merge_carts_cookies_redis(request=request, user=user, response=response)
        # 响应结果
        return response


class LogoutView(View):
    """用户退出登录"""

    def get(self, request):
        """实现用户退出登录的逻辑"""
        # 清除状态保持信息
        logout(request)
        # 退出登录后重定向到首页
        response = redirect(reverse('contents:index'))
        # 删除cookies中的用户名
        response.delete_cookie('username')

        # 响应结果
        return response


class UserInfoView(LoginRequiredMixin, View):
    """用户中心-用户信息"""

    def get(self, request):
        """提供用户中心页面"""
        # 如果LoginRequiredMixin判断出用户已登录，那么request.user就是登陆用户对象
        # 查询地址数据
        addresses = Address.objects.filter()
        address_list = []
        for address in addresses:
            address_dict = {
                "id": address.id,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
            }
            address_list.append(address_dict)
        if request.user.default_address_id==None:
            default_address='您还未设置默认地址！'
        else:
            for list in address_list:
                if list['id'] == request.user.default_address_id:
                    default_address_list = list
            default_address=default_address_list['province'] + default_address_list['city'] + default_address_list['district'] + default_address_list['place']
        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'default_address': default_address,
        }
        return render(request, 'user_center_info.html', context)


class ChangePasswordView(LoginRequiredMixin, View):
    """修改密码"""

    def get(self, request):
        # 如果LoginRequiredMixin判断出用户已登录，那么request.user就是登陆用户对象
        return render(request, 'user_center_safty.html')

    def put(self, request):
        """修改密码"""
        # 接收参数
        pwd_json_dict = json.loads(request.body.decode())
        old_password = pwd_json_dict.get('old_pwd')
        new_password = pwd_json_dict.get('new_pwd')
        new_password2 = pwd_json_dict.get('new_cpwd')
        # 验证参数
        if not all([old_password, new_password, new_password2]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_password):
            return http.HttpResponseForbidden('密码最少8位，最长20位')
        if new_password != new_password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 验证旧密码是否正确
        if not request.user.check_password(old_password):
            return render(request, 'user_center_safty.html', {'origin_password_errmsg': '原始密码错误'})
        # 修改密码
        try:
            request.user.set_password(new_password)
            request.user.save()
        except Exception as e:
            return render(request, 'user_center_safty.html', {'change_password_errmsg': '修改密码失败'})
        logout(request)
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})


class DefaultAddressView(LoginRequiredJSONMixin, View):
    """设置默认地址"""

    def put(self, reqeust, address_id):
        """实现设置默认地址逻辑"""
        try:
            # 查询出当前哪个地址会作为登录用户的默认地址
            address = Address.objects.get(id=address_id)

            # 将指定的地址设置为当前登录用户的默认地址
            reqeust.user.default_address = address
            reqeust.user.save()
        except Exception as e:
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '设置默认地址失败'})
        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '设置默认地址成功'})


class UpdateDestoryAddressView(LoginRequiredJSONMixin, View):
    """更新和删除地址"""

    def put(self, request, address_id):
        """更新地址"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')

        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('参数mobile有误')

        # 使用最新的地址信息覆盖指定的旧的地址信息
        try:
            Address.objects.filter(id=address_id).update(
                user=request.user,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
            )
        except Exception as e:
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '修改地址失败'})

        # 响应新的地址信息给前端渲染
        address = Address.objects.get(id=address_id)
        address_dict = {
            "id": address.id,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
        }
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '修改地址成功', 'address': address_dict})

    def delete(self, request, address_id):
        """删除地址"""
        # 实现指定地址的逻辑删除：is_delete=True
        try:
            address = Address.objects.get(id=address_id)
            address.is_deleted = True
            address.save()
        except Exception as e:
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '删除地址失败'})

        # 响应结果：code, errmsg
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '删除地址成功'})


class AddressCreateView(LoginRequiredJSONMixin, View):
    """新增地址"""

    def post(self, reqeust):
        """实现新增地址逻辑"""

        # 判断用户地址数量是否超过上限：查询当前登录用户的地址数量
        count = reqeust.user.addresses.count()  # 一查多，使用related_name查询
        if count > USER_ADDRESS_COUNTS_LIMIT:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '超出用户地址上限'})

        # 接收参数
        json_str = reqeust.body.decode()
        json_dict = json.loads(json_str)
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')

        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('参数mobile有误')
        # 保存用户传入的地址信息
        try:
            address = Address.objects.create(
                user=reqeust.user,
                receiver = receiver,
                province_id = province_id,
                city_id = city_id,
                district_id = district_id,
                place = place,
                mobile = mobile,
            )
            # 如果登录用户没有默认的地址，我们需要指定默认地址
            if not reqeust.user.default_address:
                reqeust.user.default_address = address
                reqeust.user.save()
        except Exception as e:
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '新增地址失败'})

        # 构造新增地址字典数据
        address_dict = {
            "id": address.id,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
        }

        # 响应新增地址结果：需要将新增的地址返回给前端渲染
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '新增地址成功', 'address': address_dict})


class AddressView(LoginRequiredMixin, View):
    """用户收货地址"""

    def get(self, request):
        """查询并展示用户地址信息"""

        # 获取当前登录用户对象
        login_user = request.user
        # 使用当前登录用户和is_deleted=False作为条件查询地址数据
        addresses = Address.objects.filter(user=login_user, is_deleted=False)
        # 将用户地址模型列表转字典列表:因为JsonResponse和Vue.js不认识模型类型，只有Django和Jinja2模板引擎认识
        address_list= []
        for address in addresses:
            address_dict = {
                "id": address.id,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
            }
            address_list.append(address_dict)
        context = {
            'username': login_user.username,
            'default_address_id': login_user.default_address_id or '0',
            'addresses': address_list,
        }
        return render(request, 'user_center_site.html', context)


class UserBrowseHistory(LoginRequiredJSONMixin, View):
    """用户浏览记录"""
    def post(self, reqeust):
        """保存用户商品浏览记录"""
        # 接收参数
        json_str = reqeust.body.decode()
        json_dict = json.loads(json_str)
        sku_id = json_dict.get('sku_id')

        # 校验参数
        try:
            Goods.objects.get(id=sku_id)
        except Goods.DoesNotExist:
            return http.HttpResponseForbidden('参数sku_id错误')

        # 保存sku_id到redis
        redis_conn = get_redis_connection('history')
        user = reqeust.user
        pl = redis_conn.pipeline()
        # 先去重
        pl.lrem('history_%s' % user.id, 0, sku_id)
        # 再保存：最近浏览的商品在最前面
        pl.lpush('history_%s' % user.id, sku_id)
        # 最后截取
        pl.ltrim('history_%s' % user.id, 0, 4)
        # 执行
        pl.execute()

        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})

    def get(self, request):
        """查询用户商品浏览记录"""
        # 获取登录用户信息
        user = request.user
        # 创建连接到redis对象
        redis_conn = get_redis_connection('history')
        # 取出列表数据（核心代码）
        sku_ids = redis_conn.lrange('history_%s' % user.id, 0, 3) # (0, 4)

        # 将模型转字典
        skus = []
        for sku_id in sku_ids:
            sku = Goods.objects.get(id=sku_id)
            skus.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url
            })
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'skus': skus})


class OrderInfoView(LoginRequiredMixin, View):
    """我的订单"""

    def get(self, request, statu_id, page_num):
        """提供我的订单页面"""
        user = request.user
        # 查询订单，按照创建时间排序
        try:
            if int(statu_id)==0:
                orders = user.orderinfo_set.all().order_by("-create_time")  # 若statu_id=0则说明查询得到所有顶订单信息
            elif int(statu_id)==6:
                orders = list(user.orderinfo_set.filter(status=int(statu_id)).order_by("-create_time"))
                orders2 = list(user.orderinfo_set.filter(status=7).order_by("-create_time"))
                orders.extend(orders2)
            else:
                orders = user.orderinfo_set.filter(status=int(statu_id)).order_by("-create_time")
        except OrderInfo.DoesNotExist:
            return http.HttpResponseForbidden('参数statu_id不存在')

        for order in orders:
            # 绑定订单状态
            order.status_name = OrderInfo.ORDER_STATUS_CHOICES[order.status - 1][1]
            # 绑定支付方式
            order.pay_method_name = OrderInfo.PAY_METHOD_CHOICES[order.pay_method - 1][1]
            order.sku_list = []
            order_goods = order.skus.all()  # 查询订单商品
            # 遍历订单商品
            for order_good in order_goods:
                sku = order_good.sku
                sku.count = order_good.count
                sku.amount = sku.price * sku.count
                order.sku_list.append(sku)
        # 分页
        page_num = int(page_num)
        try:
            # 创建分页器，对orders进行分页，每页3个数据
            paginator = Paginator(orders, 3)
            # 获取到page_num页中的记录
            page_orders = paginator.page(page_num)
            # 获取总页数：前端的分页插件需要使用
            total_page = paginator.num_pages
        except EmptyPage:
            return http.HttpResponseNotFound('订单不存在')
        context = {
            "statu_id": statu_id,
            "status": [{'id': item[0], 'name':item[1]} for item in OrderInfo.ORDER_STATUS_CHOICES[:-1]],
            "page_orders": page_orders,
            'total_page': total_page,
            'page_num': page_num,
        }
        return render(request, "user_center_order.html", context)

