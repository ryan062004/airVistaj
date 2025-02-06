from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Registration
    path('login/', views.user_login, name='login'),      # Login
    path('logout/', views.user_logout, name='logout'),   # Logout
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('delete/', views.delete_account, name='delete_account'), #Delete user's account

    path('profile/', views.profile, name='profile'),  # Profile page (update and display)
    path('membership_application/', views.membership_application, name='membership_application'),

]