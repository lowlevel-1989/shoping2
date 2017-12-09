from django.views.generic import ListView, DetailView
from django.views.generic import TemplateView
from shoping.apps.product.models import Product


class ProductListView(ListView):
    model = Product

class ProductDetailView(DetailView):
    model = Product

class CartShowView(TemplateView):
    template_name = 'shop/cart_list.html'
