from django.contrib import admin
from . import models


# admin.site.register(models.Slide)
# admin.site.register(models.Content)
# admin.site.register(models.ContentImage)


@admin.register(models.Slide)
class user_admin(admin.ModelAdmin):
    # 设置页面可以展示的字段
    list_display = ('name', 'image', 'url')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    # list_display_links = ('JOB_NAME',)
    # # 设置过滤选项
    # list_filter = ('JOB_TYPE', 'CREATED_TIME',)
    list_per_page = 20  # 每页显示条目数 缺省值100

    # def has_delete_permission(self, request, obj=None):
    #     # 禁用删除按钮
    #     return False


@admin.register(models.Content)
class user_admin(admin.ModelAdmin):
    # 设置页面可以展示的字段
    list_display = ('title', 'count', 'image')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    # list_display_links = ('JOB_NAME',)
    # # 设置过滤选项
    # list_filter = ('JOB_TYPE', 'CREATED_TIME',)
    list_per_page = 20  # 每页显示条目数 缺省值100

    # def has_delete_permission(self, request, obj=None):
    #     # 禁用删除按钮
    #     return False


@admin.register(models.ContentImage)
class user_admin(admin.ModelAdmin):
    # 设置页面可以展示的字段
    list_display = ('content', 'image', 'good_id')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    # list_display_links = ('JOB_NAME',)
    # # 设置过滤选项
    # list_filter = ('JOB_TYPE', 'CREATED_TIME',)
    list_per_page = 20  # 每页显示条目数 缺省值100

    # def has_delete_permission(self, request, obj=None):
    #     # 禁用删除按钮
    #     return False