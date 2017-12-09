from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from carton.cart import Cart
from shoping.apps.product.models import Product
from .forms import UserCreationForm

class CartShowView(TemplateView):
    template_name = 'core/cart_list.html'

class CreateUserView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/'
    http_method_names = ('get', 'post', )
