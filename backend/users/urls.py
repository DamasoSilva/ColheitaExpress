from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Autenticação
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('check-auth/', views.check_auth, name='check_auth'),
    
    # Perfil do usuário
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.UserUpdateView.as_view(), name='profile_update'),
    path('profile/detail/', views.UserProfileDetailView.as_view(), name='profile_detail'),
    path('change-password/', views.change_password_view, name='change_password'),
    
    # Dashboard
    path('dashboard-data/', views.user_dashboard_data, name='dashboard_data'),
]
