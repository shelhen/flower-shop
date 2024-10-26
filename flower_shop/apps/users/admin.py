from . import models
from django.contrib import admin

admin.site.site_header = '鲜花商城后台管理系统'  # 设置header
admin.site.site_title = '花里有话鲜花商城后台管理系统'  # 设置title
admin.site.index_title = '鲜花商城后台管理系统'


# admin.site.register(models.User)
# admin.site.register(models.Address)


@admin.register(models.User)
class user_admin(admin.ModelAdmin):
    # 设置页面可以展示的字段
    list_display = ('username', 'mobile', 'date_joined', 'is_staff', 'default_address')
    # list_editable = ('mobile',)
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = ('date_joined',)
    # list_display_links = ('JOB_NAME',)
    # # 设置过滤选项
    # list_filter = ('JOB_TYPE', 'CREATED_TIME',)
    list_per_page = 20  # 每页显示条目数 缺省值100
    # exclude = ('is_staff',)
    # # show all页面上的model数目，缺省200
    # # list_max_show_all = 200
    # # 设置可编辑字段 如果设置了可以编辑字段，页面会自动增加保存按钮

    # # 按日期月份筛选 该属性一般不用
    # # date_hierarchy = 'CREATED_TIME'
    # # 按发布日期降序排序
    # ordering = ('-CREATED_TIME',)
    # # 搜索条件设置
    # search_fields = ('JOB_NAME',)

    # def has_add_permission(self, request):
    #     # 禁用添加按钮
    #     return True
    # def has_delete_permission(self, request, obj=None):
    #     # 禁用删除按钮
    #     return False

@admin.register(models.Address)
class user_admin(admin.ModelAdmin):
    # 设置页面可以展示的字段
    list_display = ('receiver', 'province', 'city', 'district', 'place', 'mobile', 'is_deleted')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    # list_display_links = ('JOB_NAME',)
    # # 设置过滤选项
    # list_filter = ('JOB_TYPE', 'CREATED_TIME',)
    list_per_page = 20  # 每页显示条目数 缺省值100

    def has_delete_permission(self, request, obj=None):
        # 禁用删除按钮
        return False