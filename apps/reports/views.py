# apps/reports/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .utils import get_stock_report_data, get_movement_report_data, get_lowstock_report_data

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER
import io
from datetime import datetime


# ── Shared PDF helpers ──────────────────────────────────────────────────────

def _base_doc(buffer, title, landscape_mode=False):
    pagesize = landscape(letter) if landscape_mode else letter
    return SimpleDocTemplate(
        buffer,
        pagesize=pagesize,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.75*inch, bottomMargin=0.75*inch,
        title=title
    )

def _header(title):
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('T', fontSize=16, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1a1a2e'), alignment=TA_CENTER, spaceAfter=2)
    meta_style = ParagraphStyle('M', fontSize=8, fontName='Helvetica',
        textColor=colors.HexColor('#888888'), alignment=TA_CENTER, spaceAfter=10)
    return [
        Paragraph("BISMMS — Bookstore Inventory &amp; Stock Maintenance Management System", title_style),
        Paragraph(title, ParagraphStyle('ST', fontSize=12, fontName='Helvetica-Bold',
            textColor=colors.HexColor('#2c3e50'), alignment=TA_CENTER, spaceAfter=2)),
        Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}", meta_style),
        HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cccccc'), spaceAfter=12),
    ]

def _table_style(header_color='#1a1a2e'):
    return TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(header_color)),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f9f9f9'), colors.white]),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#dddddd')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ])

def _pdf_response(buffer, filename):
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


# ── Stock Report ────────────────────────────────────────────────────────────

def _export_stock_pdf(data):
    buffer = io.BytesIO()
    doc = _base_doc(buffer, 'Current Stock Report', landscape_mode=True)
    story = _header("Current Stock Report")

    # Summary row
    summary_data = [
        ['Total Book Titles', 'Low Stock Items'],
        [str(data['total_books']), str(data['total_low_stock'])],
    ]
    summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#dddddd')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TEXTCOLOR', (1,1), (1,1), colors.HexColor('#b91c1c')),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 14))

    # Main table
    headers = ['Title', 'Author', 'Category', 'Price (Rs.)', 'Quantity', 'Reorder Level', 'Status']
    rows = [headers]
    for book in data['books']:
        status = 'Low Stock' if book.is_low_stock() else 'OK'
        rows.append([
            book.title[:35],
            book.author[:20],
            str(book.category) if book.category else '—',
            str(book.price),
            str(book.quantity),
            str(book.reorder_level),
            status,
        ])

    col_widths = [2.6*inch, 1.6*inch, 1.3*inch, 1*inch, 0.8*inch, 1*inch, 0.8*inch]
    table = Table(rows, colWidths=col_widths, repeatRows=1)
    ts = _table_style()
    # Color low stock rows
    for i, book in enumerate(data['books'], start=1):
        if book.is_low_stock():
            ts.add('TEXTCOLOR', (6, i), (6, i), colors.HexColor('#b91c1c'))
            ts.add('FONTNAME', (6, i), (6, i), 'Helvetica-Bold')
    table.setStyle(ts)
    story.append(table)

    doc.build(story)
    return _pdf_response(buffer, 'stock_report.pdf')


# ── Movement Report ─────────────────────────────────────────────────────────

def _export_movement_pdf(data):
    buffer = io.BytesIO()
    doc = _base_doc(buffer, 'Stock Movement Report', landscape_mode=True)
    story = _header("Stock Movement Report")

    styles = getSampleStyleSheet()
    sub_style = ParagraphStyle('Sub', fontSize=11, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1a1a2e'), spaceBefore=12, spaceAfter=6)

    if data.get('date_from') or data.get('date_to'):
        date_range = f"Period: {data.get('date_from', 'Start') or 'Start'} to {data.get('date_to', 'Today') or 'Today'}"
        story.append(Paragraph(date_range, ParagraphStyle('DR', fontSize=9,
            fontName='Helvetica', textColor=colors.HexColor('#555555'), spaceAfter=10)))

    # Stock-In table
    story.append(Paragraph("Stock-In Records", sub_style))
    if data['stock_ins']:
        si_headers = ['Date', 'Book Title', 'Supplier', 'Quantity']
        si_rows = [si_headers]
        for r in data['stock_ins']:
            si_rows.append([
                r.created_at.strftime('%d %b %Y, %H:%M'),
                r.book.title[:40],
                str(r.supplier) if r.supplier else '—',
                str(r.quantity),
            ])
        si_table = Table(si_rows, colWidths=[1.6*inch, 4*inch, 2.2*inch, 1*inch], repeatRows=1)
        si_table.setStyle(_table_style())
        story.append(si_table)
    else:
        story.append(Paragraph("No stock-in records found.", styles['Normal']))

    story.append(Spacer(1, 16))

    # Stock-Out table
    story.append(Paragraph("Stock-Out Records", sub_style))
    if data['stock_outs']:
        so_headers = ['Date', 'Book Title', 'Quantity']
        so_rows = [so_headers]
        for r in data['stock_outs']:
            so_rows.append([
                r.created_at.strftime('%d %b %Y, %H:%M'),
                r.book.title[:40],
                str(r.quantity),
            ])
        so_table = Table(so_rows, colWidths=[1.6*inch, 5.2*inch, 1*inch], repeatRows=1)
        so_table.setStyle(_table_style())
        story.append(so_table)
    else:
        story.append(Paragraph("No stock-out records found.", styles['Normal']))

    doc.build(story)
    return _pdf_response(buffer, 'movement_report.pdf')


# ── Low Stock Report ────────────────────────────────────────────────────────

def _export_lowstock_pdf(data):
    buffer = io.BytesIO()
    doc = _base_doc(buffer, 'Low Stock Report')
    story = _header("Low Stock Report")

    if data['low_stock_books']:
        headers = ['Title', 'Author', 'Category', 'Current Qty', 'Reorder Level', 'Shortage']
        rows = [headers]
        for book in data['low_stock_books']:
            shortage = book.reorder_level - book.quantity
            rows.append([
                book.title[:38],
                book.author[:22],
                str(book.category) if book.category else '—',
                str(book.quantity),
                str(book.reorder_level),
                str(shortage),
            ])
        col_widths = [2.4*inch, 1.6*inch, 1.2*inch, 0.9*inch, 1*inch, 0.9*inch]
        table = Table(rows, colWidths=col_widths, repeatRows=1)
        ts = _table_style()
        # Highlight shortage column red
        for i in range(1, len(rows)):
            ts.add('TEXTCOLOR', (5, i), (5, i), colors.HexColor('#b91c1c'))
            ts.add('FONTNAME', (5, i), (5, i), 'Helvetica-Bold')
        table.setStyle(ts)
        story.append(table)
    else:
        styles = getSampleStyleSheet()
        story.append(Paragraph("No low stock items. All books are above reorder levels.", styles['Normal']))

    doc.build(story)
    return _pdf_response(buffer, 'lowstock_report.pdf')


# ── Views ───────────────────────────────────────────────────────────────────

@login_required
def stock_report(request):
    context = get_stock_report_data()
    if request.GET.get('export') == 'pdf':
        return _export_stock_pdf(context)
    return render(request, 'reports/stock_report.html', context)


@login_required
def movement_report(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    context = get_movement_report_data(date_from, date_to)
    if request.GET.get('export') == 'pdf':
        return _export_movement_pdf(context)
    return render(request, 'reports/movement_report.html', context)


@login_required
def lowstock_report(request):
    context = get_lowstock_report_data()
    if request.GET.get('export') == 'pdf':
        return _export_lowstock_pdf(context)
    return render(request, 'reports/lowstock_report.html', context)