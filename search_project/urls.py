# /Users/jo-jaku/Desktop/2年次/python演習/search_project/search_project/search_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('search_app.urls')),
]
