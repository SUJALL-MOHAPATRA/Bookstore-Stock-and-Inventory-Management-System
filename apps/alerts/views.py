from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import get_low_stock_books


@login_required
def alert_list(request):
    low_stock_books = get_low_stock_books()
    return render(request, 'alerts/alert_list.html', {
        'low_stock_books': low_stock_books,
    })