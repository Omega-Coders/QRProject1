from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register1),
    path('register/register', views.register),
    
]
