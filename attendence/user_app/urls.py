from django.urls import path,re_path
from . import views

urlpatterns = [
    path('/register', views.register1),
    path('register/register', views.register),
    path('login/', views.login1),
    path('login/login', views.login),
    path('register/login', views.login),

    path('signin/generate_qr', views.generate_qr),
    path('signin/generate_qr', views.generate_qr),
    path('stop' ,views.stop_qr),


   



    
]
