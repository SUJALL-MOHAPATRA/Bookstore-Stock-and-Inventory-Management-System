from django import forms
from .models import StockIn, StockOut
from apps.inventory.models import Book
from apps.suppliers.models import Supplier

class StockInForm(forms.ModelForm):
    class Meta:
        model = StockIn
        fields = ['book', 'supplier', 'quantity', 'notes']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Quantity received', 'min': 1}),
            'notes': forms.Textarea(attrs={'placeholder': 'Optional notes', 'rows': 3}),
        }

class StockOutForm(forms.ModelForm):
    class Meta:
        model = StockOut
        fields = ['book', 'quantity', 'notes']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Quantity sold', 'min': 1}),
            'notes': forms.Textarea(attrs={'placeholder': 'Optional notes', 'rows': 3}),
        }