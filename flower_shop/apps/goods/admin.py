from django.contrib import admin
from . import models


admin.site.register(models.GoodsCategory)
# admin.site.register(models.Goods)
# admin.site.register(models.GoodImage)
# admin.site.register(models.DetialImage)

@admin.register(models.Goods)
class user_admin(admin.ModelAdmin):
    # 设置页面可以展示的字段
    list_display = ('name', 'caption', 'category','price','cost_price','stock','sales','is_launched')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    # list_display_links = ('JOB_NAME',)
    # # 设置过滤选项
    # list_filter = ('JOB_TYPE', 'CREATED_TIME',)
    list_per_page =30  # 每页显示条目数 缺省值100

    # def has_delete_permission(self, request, obj=None):
    #     # 禁用删除按钮
    #     return False

@admin.register(models.GoodImage)
class user_admin(admin.ModelAdmin):
    # 设置页面可以展示的字段
    list_display = ('good', 'image')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    # list_display_links = ('JOB_NAME',)
    # # 设置过滤选项
    # list_filter = ('JOB_TYPE', 'CREATED_TIME',)
    list_per_page =20  # 每页显示条目数 缺省值100

    # def has_delete_permission(self, request, obj=None):
    #     # 禁用删除按钮
    #     return False


@admin.register(models.DetialImage)
class user_admin(admin.ModelAdmin):
    # 设置页面可以展示的字段
    list_display = ('good', 'image')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    # list_display_links = ('JOB_NAME',)
    # # 设置过滤选项
    # list_filter = ('JOB_TYPE', 'CREATED_TIME',)
    list_per_page =20  # 每页显示条目数 缺省值100

    # def has_delete_permission(self, request, obj=None):
    #     # 禁用删除按钮
    #     return False