from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.shortcuts import render

from transaction.models import Transaction
from .utils import (get_current_balance, get_total_income, get_total_expense, get_total_savings, get_this_week_range,
                    get_last_week_range, get_this_month_range, get_last_3_months_range, get_this_year_range,
                    get_income_expense_by_month, get_expense_per_category)

from identity.utils import get_admin_user

RANGE_MAP = {
    "week": get_this_week_range,
    "lweek": get_last_week_range,
    "month": get_this_month_range,
    "3months": get_last_3_months_range,
    "year": get_this_year_range,
}

@login_required(login_url='login_page')
def view_dashboard(request):
    account_admin = get_admin_user(request.user)
    current_balance = get_current_balance(request.user)

    selected_range = request.GET.get('range', 'week')
    range_func = RANGE_MAP.get(selected_range, get_this_week_range)
    start_date, end_date = range_func()

    total_income = get_total_income(account_admin, start_date, end_date)
    total_expense = get_total_expense(account_admin, start_date, end_date)
    total_savings = get_total_savings(account_admin, start_date, end_date)

    transactions = Transaction.objects.filter(Q(account_admin=account_admin) & Q(transaction_date__gte=start_date) & Q(transaction_date__lte=end_date)).order_by('-transaction_date')[:5]

    labels,income_data, expense_data = get_income_expense_by_month(account_admin, start_date, end_date)
    expense_category_labels, expense_category_data = get_expense_per_category(account_admin, start_date, end_date)
    return render(request, "fms/dashboard.html", {"total_income": total_income, "total_expense": total_expense, "current_balance": current_balance,
    "total_savings": total_savings, "selected_range": selected_range, "transactions":transactions, "labels": labels, "income_data":income_data, "expense_data": expense_data, "expense_category_labels":expense_category_labels,"expense_category_data":expense_category_data })

