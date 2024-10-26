from django.db import models
from flower_shop.utils.models import BaseModel
# Create your models here.


class Slide(BaseModel):
    name = models.CharField(max_length=100, verbose_name='标题')
    image = models.ImageField(null=True, blank=True, verbose_name='图片')
    url = models.CharField(null=True, max_length=300, verbose_name='内容链接')

    class Meta:
        db_table = 'tb_slide'
        verbose_name = '滑动幻灯片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Content(BaseModel):
    title = models.CharField(max_length=100, verbose_name='标题')
    intro = models.TextField(null=True, blank=True, verbose_name='简述')
    count = models.IntegerField(default=0, verbose_name='阅读量')
    image = models.ImageField(null=True, blank=True, verbose_name='图片')
    text = models.TextField(null=True, blank=True, verbose_name='内容')

    class Meta:
        db_table = 'tb_content'
        verbose_name = '花语内容'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class ContentImage(BaseModel):
    """内容图片"""
    content = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name='contents')
    image = models.ImageField(null=True, verbose_name='图片')
    good_id = models.CharField(null=True, max_length=100, verbose_name='商品id')

    class Meta:
        db_table = 'tb_content_image'
        verbose_name = '花语图片管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.content.title, self.id)

