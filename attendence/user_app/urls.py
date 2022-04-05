from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register1),
    path('register/register', views.register),
    path('login/', views.login1),
    path('login/login', views.login),
    path('register/login', views.login),


    
]
