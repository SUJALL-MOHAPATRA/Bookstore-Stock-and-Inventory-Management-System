from django import forms
from .models import Book, Category


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'isbn', 'category',
            'publisher', 'subject_course', 'edition',
            'price', 'quantity', 'reorder_level'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Book title'}),
            'author': forms.TextInput(attrs={'placeholder': 'Author name'}),
            'isbn': forms.TextInput(attrs={'placeholder': '13-digit ISBN'}),
            'publisher': forms.TextInput(attrs={'placeholder': 'Publisher name'}),
            'subject_course': forms.TextInput(attrs={'placeholder': 'e.g. Engineering, Medical'}),
            'edition': forms.TextInput(attrs={'placeholder': 'e.g. 3rd Edition'}),
            'price': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'quantity': forms.NumberInput(attrs={'placeholder': '0'}),
            'reorder_level': forms.NumberInput(attrs={'placeholder': '10'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Category name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Optional description', 'rows': 3}),
        }