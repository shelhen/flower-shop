from django.urls import re_path
from . import views

urlpatterns = [
    # 注册
    re_path(r'^register/$', views.RegisterView.as_view(), name='register'),
    # 判断用户名是否重复注册
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view()),
    re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    # 用户账号登录/退出登录
    re_path(r'^login/$', views.LoginView.as_view(), name='login'),
    re_path(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    # 会员中心用户信息展示
    re_path(r'^info/$', views.UserInfoView.as_view(), name='info'),
    # 修改密码
    re_path(r'^password/', views.ChangePasswordView.as_view(), name='password'),
    # 用户地址管理
    re_path(r'^addresses/$', views.AddressView.as_view(), name='address'),
    # 新增用户地址
    re_path(r'^addresses/create/$', views.AddressCreateView.as_view()),
    # 更新和删除地址
    re_path(r'^addresses/(?P<address_id>\d+)/$', views.UpdateDestoryAddressView.as_view()),
    # 设置默认地址
    re_path(r'^addresses/(?P<address_id>\d+)/default/$', views.DefaultAddressView.as_view()),
    # 用户商品浏览记录
    re_path(r'^browse_histories/$', views.UserBrowseHistory.as_view()),
    # 用户中心——订单管理
    re_path(r'^orders/(?P<statu_id>\d+)/(?P<page_num>\d+)/$', views.OrderInfoView.as_view(), name='orders'),
]