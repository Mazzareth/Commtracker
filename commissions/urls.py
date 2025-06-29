from django.urls import path
from . import views

app_name = 'commissions'

urlpatterns = [
    path('', views.home, name='home'),
    path('commissions/', views.commission_list, name='commission_list'),
    path('commissions/<int:pk>/', views.commission_detail, name='commission_detail'),

    # Client management
    path('clients/', views.client_list, name='client_list'),
    path('clients/add/', views.client_create, name='client_create'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    path('clients/<int:pk>/add-commission/', views.commission_create_for_client, name='commission_create_for_client'),
    path('clients/<int:pk>/add-character/', views.character_create_for_client, name='character_create_for_client'),
]