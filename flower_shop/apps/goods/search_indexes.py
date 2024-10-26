from haystack import indexes
from .models import SKU


class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """SKU索引数据模型类"""
    # 接收索引字段：使用文档定义索引字段，并且使用模板语法渲染
    text = indexes.CharField(document=True, use_template=True)
    # print(text)

    def get_model(self):
        """返回建立索引的模型类"""
        return SKU

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter(is_launched=True)
    # print(index_queryset())