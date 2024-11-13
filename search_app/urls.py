from django.urls import path
from . import views
from .views import login_view, logout_view, signup_view
from .views import HomeView
from .views import mercari_search
from .views import favorite_view
from .views import add_to_favorites, show_favorites

urlpatterns = [
    # ホームページ（トップページ）
    path('', HomeView.as_view(), name='home'),
    
    # 検索ページ
    path('search/', views.search_view, name='search'),  # 明示的に 'search_view' に変更

    # 商品関連のURL
    path('product/new/', views.product_create, name='product_create'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/', views.product_update, name='product_update'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('product/', views.product_list, name='product_list'),
    path('product/detail/<int:pk>/', views.product_detail, name='product_detail'),  # 商品詳細ページ


    # ログイン・ログアウト・サインアップ
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),

    # メルカリ検索
    path('mercari_search/', mercari_search, name='mercari_search'),

    # お気に入り関連のURL
    path('favorite/', favorite_view, name='favorite'),  # お気に入りリストの表示
    path('add_to_favorites/', add_to_favorites, name='add_to_favorites'),  # お気に入り追加
    path('favorites/', show_favorites, name='show_favorites'),  # お気に入り表示ページ
    path('remove_from_favorites/<int:pk>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('edit_favorite/<int:pk>/', views.edit_favorite, name='edit_favorite'),  # 編集ページのURL
    path('favorite/remove/<int:pk>/', views.remove_from_favorites, name='remove_from_favorites'),  # 削除処理
    path('favorite/', views.favorite_list, name='favorite_list'),

]
