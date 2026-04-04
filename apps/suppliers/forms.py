from django import forms
from .models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'phone', 'email', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Publisher or distributor name'}),
            'contact_person': forms.TextInput(attrs={'placeholder': 'Contact person name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email address'}),
            'address': forms.Textarea(attrs={'placeholder': 'Address', 'rows': 3}),
        }