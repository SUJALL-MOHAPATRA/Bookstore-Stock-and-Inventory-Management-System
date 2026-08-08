from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('in/', views.stockin_form, name='stockin_form'),
    path('out/', views.stockout_form, name='stockout_form'),
    path('history/', views.stock_history, name='stock_history'),
]