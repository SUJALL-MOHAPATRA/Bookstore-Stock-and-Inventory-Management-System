from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.inventory.models import Book

@login_required
def alert_list(request):
    books = Book.objects.select_related('category').all()
    low_stock_books = [book for book in books if book.is_low_stock()]
    return render(request, 'alerts/alert_list.html', {
        'low_stock_books': low_stock_books,
        'total_low_stock': len(low_stock_books),
    })