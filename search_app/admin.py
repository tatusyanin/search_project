from django.contrib import admin
from .models import Product, Category  # Category モデルをインポート

from .models import Product
admin.site.register(Product)
admin.site.register(Category)  # カテゴリモデルを管理画面に登録
