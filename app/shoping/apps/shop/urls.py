from django.urls import path
from shoping.apps.carshop.views import CarShopListView
from .views import ItemListView, ItemDetailView

urlpatterns = [
    path('', ItemListView.as_view(), name='home'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('carshop/', CarShopListView.as_view(), name='carshop'),
]
