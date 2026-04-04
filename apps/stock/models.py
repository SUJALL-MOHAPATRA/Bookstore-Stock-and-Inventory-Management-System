from django.db import models
from apps.inventory.models import Book
from apps.suppliers.models import Supplier

class StockIn(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='stock_ins')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stock-In: {self.book.title} x{self.quantity} on {self.created_at.date()}"

class StockOut(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='stock_outs')
    quantity = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stock-Out: {self.book.title} x{self.quantity} on {self.created_at.date()}"