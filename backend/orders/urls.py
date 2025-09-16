from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Pedidos
    path('', views.OrderListView.as_view(), name='order_list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    
    # Carrinho
    path('cart/calculate/', views.calculate_cart_total, name='calculate_cart_total'),
]
