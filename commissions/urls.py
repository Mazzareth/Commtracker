from django.urls import path
from . import views

app_name = 'commissions'

urlpatterns = [
    path('', views.home, name='home'),
    path('commissions/', views.commission_list, name='commission_list'),
    path('commissions/<int:pk>/', views.commission_detail, name='commission_detail'),
]