#stock\views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StockIn, StockOut
from .forms import StockInForm, StockOutForm
from apps.inventory.models import Book


@login_required
def stockin_form(request):
    if request.method == 'POST':
        form = StockInForm(request.POST)
        if form.is_valid():
            stock_in = form.save()
            # Update book quantity
            book = stock_in.book
            book.quantity += stock_in.quantity
            book.save()
            messages.success(request, f'Stock-In recorded. {book.title} quantity updated to {book.quantity}.')
            return redirect('stock:stock_history')
    else:
        form = StockInForm()
    return render(request, 'stock/stockin_form.html', {'form': form})


@login_required
def stockout_form(request):
    if request.method == 'POST':
        form = StockOutForm(request.POST)
        if form.is_valid():
            stock_out = form.save(commit=False)
            book = stock_out.book
            # Check sufficient stock
            if stock_out.quantity > book.quantity:
                messages.error(request, f'Insufficient stock. Only {book.quantity} copies available.')
                return render(request, 'stock/stockout_form.html', {'form': form})
            stock_out.save()
            book.quantity -= stock_out.quantity
            book.save()
            # Check low stock alert
            if book.is_low_stock():
                messages.warning(request, f'Low stock alert: {book.title} has only {book.quantity} copies left.')
            else:
                messages.success(request, f'Stock-Out recorded. {book.title} quantity updated to {book.quantity}.')
            return redirect('stock:stock_history')
    else:
        form = StockOutForm()
    return render(request, 'stock/stockout_form.html', {'form': form})


@login_required
def stock_history(request):
    stock_ins = StockIn.objects.select_related('book', 'supplier').order_by('-created_at')
    stock_outs = StockOut.objects.select_related('book').order_by('-created_at')
    return render(request, 'stock/stock_history.html', {
        'stock_ins': stock_ins,
        'stock_outs': stock_outs,
    })


from django.shortcuts import render

# Create your views here.
