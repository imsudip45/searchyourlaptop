from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # This maps the root URL to the home view
    path('search/', views.search_laptops, name='search_laptops'),  # Update this line for the search functionality
]
