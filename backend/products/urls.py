from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Departamentos
    path('departments/', views.DepartmentListCreateView.as_view(), name='department_list_create'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    path('departments/<int:department_id>/products/', views.products_by_department, name='products_by_department'),
    
    # Produtos
    path('', views.ProductListView.as_view(), name='product_list'),
    path('featured/', views.featured_products, name='featured_products'),

    path('create/', views.ProductCreateView.as_view(), name='product_create'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    # Estoque
    path('inventory/movement/', views.inventory_movement, name='inventory_movement'),
]
