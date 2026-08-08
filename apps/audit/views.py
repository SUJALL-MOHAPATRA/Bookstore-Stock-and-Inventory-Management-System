# apps/audit/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AuditLog


@login_required
def audit_log_list(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    logs = AuditLog.objects.select_related('user').all()
    return render(request, 'audit/audit_log.html', {'logs': logs})