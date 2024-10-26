from django.db import models
from flower_shop.utils.models import BaseModel
# Create your models here.


class GoodsCategory(BaseModel):
    """商品类别"""
    name = models.CharField(max_length=10, verbose_name='名称')

    class Meta:
        db_table = 'tb_goods_category'
        verbose_name = '类别管理'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
class Goods(BaseModel):
    """商品"""
    name = models.CharField(max_length=50, verbose_name='名称')
    intro = models.CharField(max_length=80, default='', verbose_name='简述')
    caption = models.CharField(default='2023热卖款',max_length=100, verbose_name='副标题')
    category = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, verbose_name='从属类别')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='进价')
    market_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='市场价')
    stock = models.IntegerField(null=True, verbose_name='库存')
    sales = models.IntegerField(null=True, verbose_name='销量')
    sales2 = models.CharField(max_length=50, default='', verbose_name='销量2')
    comments = models.IntegerField(null=True, verbose_name='评价数')
    material = models.TextField(null=True, verbose_name='材料信息')
    desc_detail = models.TextField(null=True, verbose_name='花语')
    desc_pack = models.TextField(null=True, verbose_name='包装信息')
    is_launched = models.BooleanField(default=True, verbose_name='是否上架销售')
    default_image = models.ImageField(max_length=200, null=True, blank=True, verbose_name='默认图片')

    class Meta:
        db_table = 'tb_goods'
        verbose_name = '商品管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.name)

class GoodImage(BaseModel):
    """商品图片"""
    good = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='goods')
    image = models.ImageField(null=True, verbose_name='图片')

    class Meta:
        db_table = 'tb_good_image'
        verbose_name = '商品图片管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.good.name, self.id)


class DetialImage(BaseModel):
    """商品图片"""
    good = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='goods')
    image = models.ImageField(null=True, verbose_name='图片')

    class Meta:
        db_table = 'tb_detail_image'
        verbose_name = '详情图片管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.good.name, self.id)
class GoodsVisitCount(BaseModel):
    """统计分类商品访问量模型类"""
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name='商品分类')
    count = models.IntegerField(verbose_name='访问量', default=0)
    date = models.DateField(auto_now_add=True, verbose_name='统计日期')

    class Meta:
        db_table = 'tb_goods_visit'
        verbose_name = '统计分类商品访问量'
        verbose_name_plural = verbose_name