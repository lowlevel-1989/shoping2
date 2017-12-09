from django.urls import path
from .views import ProductListView, ProductDetailView
from .views import CartShowView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    path('cart/show/', CartShowView.as_view(), name='carton-show'),
]
