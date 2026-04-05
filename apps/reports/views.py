from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import get_stock_report_data, get_movement_report_data, get_lowstock_report_data


@login_required
def stock_report(request):
    context = get_stock_report_data()
    return render(request, 'reports/stock_report.html', context)


@login_required
def movement_report(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    context = get_movement_report_data(date_from, date_to)
    return render(request, 'reports/movement_report.html', context)


@login_required
def lowstock_report(request):
    context = get_lowstock_report_data()
    return render(request, 'reports/lowstock_report.html', context)