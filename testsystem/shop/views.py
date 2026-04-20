import dotenv
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from .exception import exception_stripe, not_found_item

# Create your views here.
from .models import Item
from .serializers import ItemSerializer

dotenv.load_dotenv()


class ItemView:
    @staticmethod
    def get_items(request: HttpRequest) -> HttpResponse:
        items = Item.objects.all()
        data = ItemSerializer(items).data
        return render(request, "index.html", context=data)

    @staticmethod
    @not_found_item
    def get_item_by_id(request: HttpRequest, item_id: int) -> HttpResponse:
        item = Item.objects.get(pk=item_id)
        return render(request, "item.html", context=ItemSerializer(item).data)

    @staticmethod
    @exception_stripe
    @not_found_item
    def buy_item_by_id(request: HttpRequest, item_id: int) -> HttpResponse:
        import stripe

        instance_item = Item.objects.get(pk=item_id)
        checkout_session = stripe.checkout.Session.create(
            success_url=f"http://localhost:8000/item/{item_id}",
            cancel_url=f"http://localhost:8000/item/{item_id}",
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(instance_item.price * 100),
                        "product_data": {
                            "name": instance_item.name,
                            "description": instance_item.description,
                        },
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
        )
        return JsonResponse({"session_url": checkout_session.url})
