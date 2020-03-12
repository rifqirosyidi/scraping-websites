from django.urls import path, include
from . import views

app_name = 'flash_it'
urlpatterns = [
    path('flashsale/', views.flashsale, name="flashsale"),
]
