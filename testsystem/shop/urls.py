from django.contrib import admin
from django.urls import path, include, re_path
from shop import urls as shop_urls
from .views import ItemView

urlpatterns = [
    path('item/', ItemView.get_items, name="items"),
    re_path(r'^item/(?P<item_id>\d+)', ItemView.get_item_by_id, name='item'),
    re_path(r'^buy/(?P<item_id>\d+)', ItemView.buy_item_by_id, name='buy_item'),
]
