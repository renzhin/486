from django.urls import path

from . import views

app_name = 'cpus'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('cpus_list/', views.cpus_list, name='cpus_list'),
    path('cpu_detail/<int:pk>/', views.cpu_detail, name='cpu_detail'),
    path('user_cpus/<int:pk>/', views.user_cpus, name='user_cpus'),
    # path('cpu_add', views.cpu_add_edit, name='cpu_add'),
    path('cpu_add/', views.CpuCreateView.as_view(), name='cpu_add'),
    path('cpu_detail/<int:pk>/edit/', views.cpu_add_edit, name='cpu_edit'),
    path('cpu_detail/<int:pk>/delete/', views.cpu_delete, name='cpu_delete'),
]
