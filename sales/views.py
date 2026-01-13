from django.shortcuts import render
from django.db.models import Sum
from datetime import date
from .models import Sale, Expense
from .forms import SaleForm
from django.shortcuts import redirect
from datetime import datetime
from django.db.models.functions import TruncMonth
import openpyxl
from django.http import HttpResponse

def daily_dashboard(request):
    today = date.today()

    sales = Sale.objects.filter(date=today)

    product_summary = []
    total_sales = 0
    total_cost = 0
    total_commission = 0

    for sale in sales:
        sales_amount = sale.total_sales_amount()
        cost = sale.total_cost()
        commission = sale.total_commission()
        profit = sale.profit()

        product_summary.append({
            'product': sale.product.name,
            'quantity': sale.quantity,
            'sales': sales_amount,
            'cost': cost,
            'commission': commission,
            'profit': profit,
        })

        total_sales += sales_amount
        total_cost += cost
        total_commission += commission

    expenses = Expense.objects.filter(date=today)
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0

    net_profit = total_sales - total_cost - total_commission - total_expenses

    context = {
        'today': today,
        'product_summary': product_summary,
        'total_sales': total_sales,
        'total_cost': total_cost,
        'total_commission': total_commission,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
    }

    return render(request, 'sales/dashboard.html', context)


def add_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('daily_dashboard')
    else:
        form = SaleForm()

    return render(request, 'sales/add_sale.html', {'form': form})

def daily_dashboard(request):
    selected_date = request.GET.get('date')

    if selected_date:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    else:
        selected_date = date.today()

    sales = Sale.objects.filter(date=selected_date)

    product_summary = []
    total_sales = 0
    total_cost = 0
    total_commission = 0

    for sale in sales:
        sales_amount = sale.total_sales_amount()
        cost = sale.total_cost()
        commission = sale.total_commission()
        profit = sale.profit()

        product_summary.append({
            'product': sale.product.name,
            'quantity': sale.quantity,
            'sales': sales_amount,
            'cost': cost,
            'commission': commission,
            'profit': profit,
        })

        total_sales += sales_amount
        total_cost += cost
        total_commission += commission

    expenses = Expense.objects.filter(date=selected_date)
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0

    net_profit = total_sales - total_cost - total_commission - total_expenses

    context = {
        'today': selected_date,
        'product_summary': product_summary,
        'total_sales': total_sales,
        'total_cost': total_cost,
        'total_commission': total_commission,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
    }

    return render(request, 'sales/dashboard.html', context)

def monthly_report(request):
    sales = Sale.objects.annotate(month=TruncMonth('date')).values('month').annotate(
        total_sales=Sum('quantity')
    )

    return render(request, 'sales/monthly.html', {'sales': sales})

def export_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Product', 'Quantity', 'Profit'])

    for sale in Sale.objects.all():
        ws.append([
            sale.product.name,
            sale.quantity,
            sale.profit()
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=report.xlsx'
    wb.save(response)
    return response