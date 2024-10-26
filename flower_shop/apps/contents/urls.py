from django.urls import re_path
from . import views

urlpatterns = [
    # 首页视图
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    # 花语列表页
    re_path(r'^flowerylist/(?P<page_num>\d+)/$', views.FloweryListView.as_view()),
    # 花语详情
    re_path(r'^flowery/(?P<content_id>\d+)/$', views.FloweryView.as_view(), name='flowery'),
    # 热门评论
    re_path(r'^rank/$', views.HotFloweryView.as_view()),
    # 后台管理系统控制面板
    re_path(r'^dashboard/(?P<page_num>\d+)/$', views.DashBoardView.as_view(), name='dashboard'),
]