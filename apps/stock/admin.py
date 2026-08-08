from django.contrib import admin
from .models import StockIn, StockOut

@admin.register(StockIn)
class StockInAdmin(admin.ModelAdmin):
    list_display = ['book', 'supplier', 'quantity', 'created_at']
    list_filter = ['created_at']
    search_fields = ['book__title']

@admin.register(StockOut)
class StockOutAdmin(admin.ModelAdmin):
    list_display = ['book', 'quantity', 'created_at']
    list_filter = ['created_at']
    search_fields = ['book__title']