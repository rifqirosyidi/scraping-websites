from django.urls import path
from . import views

app_name = 'find_it'
urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about')
]
