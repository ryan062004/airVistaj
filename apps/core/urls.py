# core/urls.py

from django.urls import path
from . import views
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage  # Add this import

urlpatterns = [
    # PAGES
    path('', views.home, name='home'), #HOME PAGE
    path('about/', views.about, name='about'), #ABOUT PAGE

    path('members/', views.members_list, name='members'),
]
