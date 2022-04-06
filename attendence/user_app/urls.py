from django.urls import path,re_path
from . import views

urlpatterns = [
    path('register/', views.register1),
    path('register/register', views.register),
    path('login/', views.login1),
    path('login/login', views.login),
    path('register/login', views.login),

    path('login/generate_qr', views.generate_qr),
    path('register/generate_qr', views.generate_qr),


   re_path(r'^All_QR_codes/(?P<temp>[\w-]+)',views.get_qr),



    
]
