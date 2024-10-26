from django.urls import re_path
from . import views


urlpatterns = [
    # 省市区三级联动
    re_path(r'^areas/$', views.AreasView.as_view()),
]