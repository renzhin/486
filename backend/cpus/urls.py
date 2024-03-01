from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('about/', views.about),
    path('cpus_list/', views.cpus_list),
    path('cpu_detail/<int:pk>/', views.cpu_detail),
]
