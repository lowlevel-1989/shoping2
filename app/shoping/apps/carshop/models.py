import json

class CarShop(object):

    def __init__(self, request):
        self._items = json.loads(request.COOKIES.get('items', '[]'))

    def get(self, pk=None):
        items = self._items[pk] if pk and self._items.get(pk) else self._items
        return items

    def delete(self, pk):
        del self._items[pk]

    def add(self, obj):
        self._items[obj.pk] = obj
        return self._items

    def save(self, response):
        response.set_cookie('items', json.dumps(self._items))
        return response
