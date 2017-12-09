import json
from django.views.generic import TemplateView
from shoping.apps.shop.models import Item

class CarShopListView(TemplateView):
    template_name = 'carshop/item_list.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        enc_items__pk = request.COOKIES.get('items__pk', '[]') # list pk
        enc_items__qt = request.COOKIES.get('items__qt', '[]') # list quantity
        enc_items__tl = request.COOKIES.get('items__tl', 0) # total
        items__pk = set(json.loads(enc_items__pk))
        items__qt = json.loads(enc_items__qt)
        items = Item.objects.filter(pk__in=items__pk)

        context['object_list'] = items
        context['object_qt_list'] = items__qt
        context['total'] = enc_items__tl
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        enc_items__pk = request.COOKIES.get('items__pk', '[]') # list pk
        enc_items__qt = request.COOKIES.get('items__qt') # list quantity
        enc_items__tl = request.COOKIES.get('items__tl', 0) # total
        items__pk = set(json.loads(enc_items__pk))

        items__qt = dict()
        if enc_items__qt:
            items__qt = json.loads(enc_items__qt)

        action = request.POST.get('action')
        item__pk = int(request.POST.get('item'))
        item__qt = int(request.POST.get('quantity'))

        cache_list = set()
        total = 0
        if action == 'add':
            items__pk.add(item__pk) # agrego el item a la lista
            items__qt[str(item__pk)] = item__qt # agrego su cantidad
            for i in items__pk:
                item = Item.objects.filter(pk=i).first()
                if item:
                    total += (items__qt[str(item.pk)] * item.price)
                    cache_list.add(item.pk)
        else:
            total = enc_items__tl

        items = Item.objects.filter(pk__in=cache_list)

        context['object_list'] = items
        context['object_qt_list'] = items__qt
        context['total'] = total

        response = self.render_to_response(context)
        response.set_cookie('items__pk', json.dumps(list(cache_list)))
        response.set_cookie('items__qt', json.dumps(items__qt))
        response.set_cookie('items__tl', total)
        return response



