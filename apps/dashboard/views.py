from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.inventory.models import Book
from apps.stock.models import StockIn, StockOut

@login_required
def index(request):
    books = Book.objects.all()
    total_books = books.count()
    low_stock_books = [book for book in books if book.is_low_stock()]
    total_low_stock = len(low_stock_books)
    total_stock_value = sum(book.price * book.quantity for book in books)

    recent_stock_ins = StockIn.objects.select_related('book').order_by('-created_at')[:5]
    recent_stock_outs = StockOut.objects.select_related('book').order_by('-created_at')[:5]

    return render(request, 'dashboard/index.html', {
        'total_books': total_books,
        'total_low_stock': total_low_stock,
        'total_stock_value': total_stock_value,
        'recent_stock_ins': recent_stock_ins,
        'recent_stock_outs': recent_stock_outs,
    })