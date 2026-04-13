from apps.inventory.models import Book
from apps.accounts.models import CustomUser
from django.core.mail import send_mail
from django.conf import settings


def get_low_stock_books():
    books = Book.objects.select_related('category').all()
    return [book for book in books if book.is_low_stock()]


def get_low_stock_count():
    return len(get_low_stock_books())


def send_low_stock_email(book):
    # Get all active Admin and Manager emails
    recipients = CustomUser.objects.filter(
        role__in=['admin', 'manager'],
        is_active=True,
        email__isnull=False
    ).exclude(email='').values_list('email', flat=True)

    if not recipients:
        return

    subject = f'Low Stock Alert — {book.title}'
    message = (
        f'This is an automated alert from BISMMS.\n\n'
        f'The following book has fallen below its reorder level:\n\n'
        f'  Title     : {book.title}\n'
        f'  Author    : {book.author}\n'
        f'  ISBN      : {book.isbn}\n'
        f'  Current Stock : {book.quantity} copies\n'
        f'  Reorder Level : {book.reorder_level} copies\n\n'
        f'Please arrange restocking at the earliest.\n\n'
        f'— BISMMS Automated Alert System'
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=list(recipients),
        fail_silently=True,
    )