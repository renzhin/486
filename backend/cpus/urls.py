from django.urls import path

from . import views

app_name = 'cpus'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('cpus_list/', views.cpus_list, name='cpus_list'),
    path('cpu_detail/<int:pk>/', views.cpu_detail, name='cpu_detail'),
]
