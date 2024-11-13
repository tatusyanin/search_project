from django import forms
from .models import Product  # Productモデルが定義されていることを確認

class SearchForm(forms.Form):
      query = forms.CharField(
      label='検索キーワード',
      max_length=100, # CharField で max_length が有効です
      required=False,
      widget=forms.TextInput(attrs={'placeholder': '検索したいキーワードを入力'})
)
      
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']

from .models import Favorite  # Favoriteモデルをインポート

class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ['name', 'price', 'url']

class FavoriteEditForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ['name', 'price', 'url']  # 編集可能なフィールドを指定