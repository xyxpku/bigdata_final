"""communication1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from robot_communication import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index/', views.index),
    path('loginf/', views.loginf),
    path('regist/', views.regist),
    path('robot_response/', views.robot_response),
    path('logoutf/', views.logoutf),
    path('delete_all/', views.delete_all),
    path('robot_response_2/', views.robot_response_2),
    path('delete_all_2/', views.delete_all_2),
    # path('ajax_add/', views.ajax_add),
    # path('ajax_demo1/', views.ajax_demo1),
]
