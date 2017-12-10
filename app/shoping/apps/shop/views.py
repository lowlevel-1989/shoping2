import logging
from django.views.generic import ListView, DetailView
from django.views.generic import TemplateView
from carton.cart import Cart
from shoping.apps.product.models import Product

logger = logging.getLogger(__name__)

class ProductListView(ListView):
    model = Product

class ProductDetailView(DetailView):
    model = Product

class CartShowView(TemplateView):
    template_name = 'shop/cart_list.html'

    def get(self, request, *args, **kwargs):
        logger.debug(request.session.items())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        cart = Cart(request.session)
        delete = request.POST.get('action') == 'delete'
        product = Product.objects.get(pk=request.POST.get('product'))
        quantity = request.POST.get('quantity', 1)
        price = product.price
        if delete:
            cart.remove(product)
        else:
            cart.add(product, price, quantity)
        return super().get(request, *args, **kwargs)

