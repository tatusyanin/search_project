from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category  # Product モデルをインポート
from .forms import SearchForm, ProductForm  # ProductForm もインポート
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# views.py
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # 商品を保存
            product = form.save()

            # 商品をお気に入りに追加
            favorite = Favorite(
                user=request.user,
                name=product.name,
                price=product.price,
                url=product.url  # 必要なURLを指定
            )
            favorite.save()

            # 成功メッセージ
            messages.success(request, "商品を追加し、お気に入りにも追加しました。")
            return redirect('product_list')  # 商品一覧ページへリダイレクト

    else:
        form = ProductForm()

    return render(request, 'product/product_create.html', {'form': form})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'search_app/product_detail.html', {'product': product})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'product_form.html', {'form': form, 'product': product})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    print(f"Deleting product: {product.name}")  # デバッグ用出力
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'search_app/product_confirm_delete.html', {'product': product})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def search_view(request):
    form = SearchForm(request.GET or None)
    results = Product.objects.all()  # クエリセットの初期化
    categories = Category.objects.all()  # カテゴリをデータベースから取得
 # 検索条件のフィルタリング
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            results = results.filter(name__icontains=query)  # 商品名でフィルタリング

    # カテゴリフィルタリング
    category_name = request.GET.get('category')
    if category_name:
        try:
            # カテゴリ名に基づいてカテゴリ ID を取得
            category = Category.objects.get(name=category_name)
            results = results.filter(category_id=category.id)
        except Category.DoesNotExist:
            results = results.none()  # 存在しないカテゴリの場合、結果を空にする
            category = None

    # 価格のフィルタリング(最低価格・最高価格)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    try:
        if min_price:
            results = results.filter(price__gte=min_price)
        if max_price:
            results = results.filter(price__lte=max_price)  
    except ValueError:
        results = results.none()

    # 並び替え処理
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_asc':
        results = results.order_by('price')
    elif sort_by == 'price_desc':
        results = results.order_by('-price')

    # Paginator の設定
    paginator = Paginator(results, 11)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search_app/search.html', {
        'form': form,
        'page_obj': page_obj,
        'results': results,  # 結果を渡す
        'categories': categories,  # カテゴリを渡す

    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # サインイン後のリダイレクト先
        else:
            messages.error(request, 'ユーザー名またはパスワードが間違っています。')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')  # サインアウト後のリダイレクト先

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}として登録されました。')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

from django.views.generic import TemplateView  # 必要なインポート

class HomeView(TemplateView):
    template_name = 'home.html'  # 使用するテンプレート名

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 必要なコンテキストデータを追加
        return context


import requests  # ここにインポートを追加

def mercari_search(request):
    url = 'https://api.mercari.jp/items/search'
    
    # 商品名をリクエストから取得（例: queryパラメータ）
    product_name = request.GET.get('query', '商品名')  # デフォルトの値を設定
    
    params = {
        'keyword': product_name,  # 正しいパラメータ名に変更
        'limit': 1000             # 取得する商品の数
    }

    # リクエストの送信
    try:
        response = requests.get(url, params=params)

        # ステータスコードのチェック
        if response.status_code == 200:
            # 成功した場合、JSON形式でレスポンスを取得
            data = response.json()
            print("APIレスポンス:", data)  # レスポンス全体を表示
            
            items = []
            # 'items'キーの存在を確認
            if 'items' in data:
                items = data['items']
            else:
                print("itemsキーが存在しません:", data)
            
            # テンプレートにデータを渡してレスポンスを返す
            return render(request, 'search_app/mercari_search.html', {'items': items})

        else:
            print(f"エラーが発生しました: {response.status_code}, メッセージ: {response.text}")
            messages.error(request, f"エラーが発生しました: {response.status_code}, メッセージ: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"リクエストエラーが発生しました: {e}")
        messages.error(request, "リクエストエラーが発生しました。")

    # 何らかのエラーが発生した場合、空のリストを返す
    return render(request, 'search_app/mercari_search.html', {'items': []})

from .models import Favorite
from django.contrib.auth.decorators import login_required
from .forms import FavoriteForm  # お使いのフォームをインポート


from .models import Favorite
from django.http import HttpResponse, JsonResponse
from decimal import Decimal
from .forms import FavoriteEditForm

@login_required
def add_to_favorites(request):
    name = request.POST.get('item_name')
    price = request.POST.get('item_price')
    url = request.POST.get('item_url')

    # 入力値が正しいか確認
    if not name or not price or not url:
        messages.error(request, "必要な情報が不足しています。")
        return redirect('search_view')  # 例えば検索結果ページにリダイレクト

    # ログインしている場合のみお気に入りに追加
    if request.user.is_authenticated:
        favorite = Favorite(user=request.user, name=name, price=price, url=url)
        favorite.save()
        messages.success(request, "お気に入りに追加しました。")
        return redirect('favorite')  # お気に入りページにリダイレクト
    else:
        # ログインしていない場合は、ログインページへリダイレクト
        return redirect('login')






def favorite_view(request):
    favorites = Favorite.objects.all()  # 全てのお気に入りを取得
    return render(request, 'favorites/show_favorites.html', {'favorites': favorites})



@login_required
def favorite_list(request):
    # ログインしているユーザーのみに絞る
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
        return render(request, 'favorite_list.html', {'favorites': favorites})
    else:
        return redirect('login')


@login_required  # ユーザーが認証されていることを要求
def show_favorites(request):
    # ログインしているユーザーの、お気に入りリストを取得
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
    else:
        favorites = []
        messages.error(request, "ログインしていないため、お気に入りを表示できません。")
    
    return render(request, 'show_favorite.html', {'favorites': favorites})

def favorite_view(request):
    # ログインしているユーザーのお気に入りを取得
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
    else:
        favorites = []

    return render(request, 'product/show_favorite.html', {'favorites': favorites})

def edit_favorite(request, pk):
    favorite = get_object_or_404(Favorite, pk=pk)

    if request.method == 'POST':
        form = FavoriteEditForm(request.POST, instance=favorite)
        if form.is_valid():
            form.save()
            return redirect('favorite')  # 編集後はお気に入り一覧ページにリダイレクト
    else:
        form = FavoriteEditForm(instance=favorite)

    return render(request, 'favorites/edit_favorite.html', {'form': form})
from django.urls import reverse

@login_required
def remove_from_favorites(request, pk):
    favorite = get_object_or_404(Favorite, pk=pk)  # 削除対象のアイテムを取得
    if request.method == 'POST':
        favorite.delete()  # お気に入りから削除
        return redirect('favorite_list')  # 削除後にお気に入り一覧ページにリダイレクト
    return redirect('favorite_list')  # GETリクエストの場合もリストページに戻る

from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def save_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order = data.get('order', [])

        # 順序を保存するロジック（例: データベースの更新）
        # models.FavoriteItem.objects.bulk_update(order)

        return JsonResponse({'status': 'success', 'order': order})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)