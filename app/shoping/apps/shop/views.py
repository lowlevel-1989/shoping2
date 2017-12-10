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
        action = request.POST.get('action')
        delete = action == 'delete'
        clear = action == 'clear'

        cart = Cart(request.session)
        product = Product.objects.filter(pk=request.POST.get('product')).first()
        quantity = request.POST.get('quantity', 1)

        if delete:
            cart.remove(product)
        elif clear:
            cart.clear()
        else:
            cart.add(product, product.price, quantity)
        return super().get(request, *args, **kwargs)

