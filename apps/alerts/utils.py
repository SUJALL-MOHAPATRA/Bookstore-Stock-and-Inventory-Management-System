from apps.inventory.models import Book


def get_low_stock_books():
    books = Book.objects.select_related('category').all()
    return [book for book in books if book.is_low_stock()]


def get_low_stock_count():
    return len(get_low_stock_books())