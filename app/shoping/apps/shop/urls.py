from django.urls import path
from .views import ProductListView, ProductDetailView
from .views import CartShowView, EpaycoView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    path('cart/', CartShowView.as_view(), name='carton'),
    path('in/security/', EpaycoView.as_view(), name='epayco'),
    path('in/ticket/', EpaycoView.as_view(), name='ticket'),
]
