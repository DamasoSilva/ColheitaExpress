from django.urls import path
from . import views

app_name = 'deliveries'

urlpatterns = [
    # Entregas
    path('', views.DeliveryListView.as_view(), name='delivery_list'),
    path('driver/', views.driver_deliveries, name='driver_deliveries'),
    path('<int:delivery_id>/status/', views.update_delivery_status, name='update_delivery_status'),
    
    # Rastreamento público
    path('track/<str:tracking_code>/', views.track_delivery, name='track_delivery'),
]
