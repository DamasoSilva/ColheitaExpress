from django.urls import path
from . import views
from .cart_views import CartView, AddToCartView, RemoveFromCartView, UpdateCartView, ClearCartView, CheckoutView

app_name = 'orders'

urlpatterns = [
    # Pedidos
    path('', views.OrderListView.as_view(), name='order_list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    
    # Carrinho
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/update/', UpdateCartView.as_view(), name='update_cart'),
    path('cart/clear/', ClearCartView.as_view(), name='clear_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('cart/calculate/', views.calculate_cart_total, name='calculate_cart_total'),
]
