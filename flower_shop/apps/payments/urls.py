from django.urls import re_path
from . import views


urlpatterns = [
    # 支付
    re_path(r'payment/(?P<order_id>\d+)/', views.PaymentView.as_view()),
    # 保存订单状态
    re_path(r'^payment/status/$', views.PaymentStatusView.as_view()),
    # 当用户选择货到付款时，保存订单状态
    re_path(r'^payment/paymethod/(?P<order_id>\d+)/$', views.PayMethodView.as_view())
]