from .models import Item
from django.db.models import QuerySet
class ItemSerializer:
    
    def __init__(self, item: Item | list[Item] | QuerySet):
        self._item = item
        self._many = True if isinstance(item, (list, QuerySet)) else False

        
    @property
    def data(self) -> dict:
        if self._many:
            return {"items": [
                self._get_object(item)
                for item in self._item
            ]}
        return self._get_object(self._item)
    
    def _get_object(self, item: Item):
        return {
            "id": item.pk,
            "name": item.name,
            "description": item.description,
            "price": item.price
        }