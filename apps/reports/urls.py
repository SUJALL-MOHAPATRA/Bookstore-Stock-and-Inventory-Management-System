from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.stock_report, name='stock_report'),
    path('movement/', views.movement_report, name='movement_report'),
    path('lowstock/', views.lowstock_report, name='lowstock_report'),
]