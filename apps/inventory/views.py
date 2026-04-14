# inventory/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, Category
from .forms import BookForm, CategoryForm
from apps.audit.utils import log_action


@login_required
def book_list(request):
    books = Book.objects.select_related('category').all()
    query = request.GET.get('q')
    if query:
        books = books.filter(title__icontains=query) | \
                books.filter(author__icontains=query) | \
                books.filter(isbn__icontains=query)
    return render(request, 'inventory/product_list.html', {
        'books': books,
        'query': query
    })


@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'inventory/product_detail.html', {'book': book})


@login_required
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            log_action(request.user, 'Book Added', f'"{book.title}" (ISBN: {book.isbn}) added by "{request.user.username}".')
            messages.success(request, 'Book added successfully.')
            return redirect('inventory:book_list')
    else:
        form = BookForm()
    return render(request, 'inventory/product_form.html', {
        'form': form,
        'action': 'Add'
    })


@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            log_action(request.user, 'Book Edited', f'"{book.title}" (ISBN: {book.isbn}) edited by "{request.user.username}".')
            messages.success(request, 'Book updated successfully.')
            return redirect('inventory:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'inventory/product_form.html', {
        'form': form,
        'action': 'Edit'
    })


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        log_action(request.user, 'Book Deleted', f'"{book.title}" (ISBN: {book.isbn}) deleted by "{request.user.username}".')
        book.delete()
        messages.success(request, 'Book deleted successfully.')
        return redirect('inventory:book_list')
    return render(request, 'inventory/product_detail.html', {
        'book': book,
        'confirm_delete': True
    })


@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'inventory/category_list.html', {
        'categories': categories
    })


@login_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            log_action(request.user, 'Category Added', f'Category "{category.name}" added by "{request.user.username}".')
            messages.success(request, 'Category added successfully.')
            return redirect('inventory:category_list')
    else:
        form = CategoryForm()
    return render(request, 'inventory/category_form.html', {
        'form': form,
        'action': 'Add'
    })