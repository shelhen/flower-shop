from . import models
from django.contrib import admin


# admin.site.register(models.OrderInfo)
# admin.site.register(models.OrderGoods)


@admin.register(models.OrderInfo)
class user_admin(admin.ModelAdmin):
    # 设置页面可以展示的字段
    list_display = ('order_id', 'user','address','total_count','total_amount','freight','pay_method','status')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    # list_display_links = ('JOB_NAME',)
    # # 设置过滤选项
    # list_filter = ('JOB_TYPE', 'CREATED_TIME',)
    list_per_page =20  # 每页显示条目数 缺省值100

    # def has_delete_permission(self, request, obj=None):
    #     # 禁用删除按钮
    #     return False


@admin.register(models.OrderGoods)
class user_admin(admin.ModelAdmin):
    # 设置页面可以展示的字段
    list_display = ('order', 'sku','count','price','score','is_commented','comment')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    # list_display_links = ('JOB_NAME',)
    # # 设置过滤选项
    # list_filter = ('JOB_TYPE', 'CREATED_TIME',)
    list_per_page =20  # 每页显示条目数 缺省值100

    # def has_delete_permission(self, request, obj=None):
    #     # 禁用删除按钮
    #     return False
