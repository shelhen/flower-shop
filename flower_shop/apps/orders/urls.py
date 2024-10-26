from django.urls import re_path
from . import views


urlpatterns = [
    # 结算订单
    re_path(r'^orders/settlement/$', views.OrderSettlementView.as_view(), name='settlement'),
    # 提交订单
    re_path(r'^orders/commit/$', views.OrderCommitView.as_view()),
    # 顾客提交订单评价
    re_path(r'^orders/comment/$', views.CommentView.as_view()),  # (?P<order_id>\d+)/
    # 详情页获取商品评论
    re_path(r'^comment/(?P<sku_id>\d+)/$', views.CommentSKUView.as_view()),
    # 确认收货
    re_path(r'^confirm/(?P<order_id>\d+)/', views.OrderConfirmView.as_view()),
    # 确认发货与退款
    re_path(r'^send/(?P<order_id>\d+)/(?P<status>\d+)/', views.OrderSendView.as_view()),
    # 评价晒单
    re_path(r'^user/comment/(?P<page_num>\d+)/', views.UserCommentView.as_view()),
    # 用户退款
    re_path(r'^orders/drawback/$', views.DrawbackView.as_view()),  # (?P<order_id>\d+)/
]