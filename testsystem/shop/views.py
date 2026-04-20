from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from .serializers import ItemSerializer

# Create your views here.
from .models import Item
from django.db.models import QuerySet


class ItemView:
    @staticmethod
    def get_items(request: HttpRequest) -> HttpResponse:
        items = Item.objects.all()
        data = ItemSerializer(items).data
        print(data)
        return render(request, "index.html", context=data)

    @staticmethod
    def get_item_by_id(request: HttpRequest, item_id:int) -> HttpResponse:
        try:
            item = Item.objects.get(pk=item_id)
            return render(request, "item.html", context=ItemSerializer(item).data)
        except Item.DoesNotExist:
            return HttpResponseNotFound(f"Продукт с id={item_id} не найден")