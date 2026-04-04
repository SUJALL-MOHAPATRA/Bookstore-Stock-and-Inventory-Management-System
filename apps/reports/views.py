from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from apps.inventory.models import Book
from apps.stock.models import StockIn, StockOut

@login_required
def stock_report(request):
    books = Book.objects.select_related('category').all()
    low_stock_books = [book for book in books if book.is_low_stock()]
    total_books = books.count()
    total_low_stock = len(low_stock_books)
    return render(request, 'reports/stock_report.html', {
        'books': books,
        'low_stock_books': low_stock_books,
        'total_books': total_books,
        'total_low_stock': total_low_stock,
    })

@login_required
def movement_report(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    stock_ins = StockIn.objects.select_related('book', 'supplier').order_by('-created_at')
    stock_outs = StockOut.objects.select_related('book').order_by('-created_at')

    if date_from:
        stock_ins = stock_ins.filter(created_at__date__gte=date_from)
        stock_outs = stock_outs.filter(created_at__date__gte=date_from)
    if date_to:
        stock_ins = stock_ins.filter(created_at__date__lte=date_to)
        stock_outs = stock_outs.filter(created_at__date__lte=date_to)

    return render(request, 'reports/movement_report.html', {
        'stock_ins': stock_ins,
        'stock_outs': stock_outs,
        'date_from': date_from,
        'date_to': date_to,
    })

@login_required
def lowstock_report(request):
    books = Book.objects.select_related('category').all()
    low_stock_books = [book for book in books if book.is_low_stock()]
    return render(request, 'reports/lowstock_report.html', {
        'low_stock_books': low_stock_books,
    })