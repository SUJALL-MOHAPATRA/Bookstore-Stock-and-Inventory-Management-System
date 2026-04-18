#apps\reports\utils.py
from apps.inventory.models import Book
from apps.stock.models import StockIn, StockOut


def get_stock_report_data():
    books = Book.objects.select_related('category').all()
    low_stock_books = [book for book in books if book.is_low_stock()]
    total_books = books.count()
    total_low_stock = len(low_stock_books)
    return {
        'books': books,
        'low_stock_books': low_stock_books,
        'total_books': total_books,
        'total_low_stock': total_low_stock,
    }


def get_movement_report_data(date_from=None, date_to=None):
    stock_ins = StockIn.objects.select_related('book', 'supplier').order_by('-created_at')
    stock_outs = StockOut.objects.select_related('book').order_by('-created_at')

    if date_from:
        stock_ins = stock_ins.filter(created_at__date__gte=date_from)
        stock_outs = stock_outs.filter(created_at__date__gte=date_from)
    if date_to:
        stock_ins = stock_ins.filter(created_at__date__lte=date_to)
        stock_outs = stock_outs.filter(created_at__date__lte=date_to)

    return {
        'stock_ins': stock_ins,
        'stock_outs': stock_outs,
        'date_from': date_from,
        'date_to': date_to,
    }


def get_lowstock_report_data():
    books = Book.objects.select_related('category').all()
    low_stock_books = [book for book in books if book.is_low_stock()]
    return {
        'low_stock_books': low_stock_books,
    }