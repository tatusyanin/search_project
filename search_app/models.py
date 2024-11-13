from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    url = models.URLField(max_length=200, blank=True, null=True)  # URLフィールドを追加

    def __str__(self):
        return self.name

from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    url = models.URLField(blank=True, null=True)  # オプションにする

    def __str__(self):
        return self.name
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'url']  # 必要なフィールドを指定

