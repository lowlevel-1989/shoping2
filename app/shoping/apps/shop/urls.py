from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

    path('cart/', views.CartShowView.as_view(), name='carton'),
    path('in/security/', views.EpaycoView.as_view(), name='epayco'),
    path('in/ticket/', views.EpaycoView.as_view(), name='ticket'),
    path('ticket/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
]
