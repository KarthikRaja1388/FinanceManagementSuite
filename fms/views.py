from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.aggregates import Sum

from django.shortcuts import render

from budget.utils import get_alerts, get_insights
from shopping.utils import get_most_used_category, get_weekly_spend, get_monthly_spend
from transaction.models import Transaction
from .utils import (get_current_balance, get_total_income, get_total_expense, get_total_savings, get_this_week_range,
                    get_last_week_range, get_this_month_range, get_last_3_months_range, get_this_year_range,
                    get_income_expense_by_month, get_expense_per_category, get_budget_summary)

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
    budget_summaries = get_budget_summary(account_admin)
    transactions = Transaction.objects.filter(Q(account_admin=account_admin) & Q(transaction_date__gte=start_date) & Q(transaction_date__lte=end_date)).order_by('-transaction_date')[:5]

    labels,income_data, expense_data = get_income_expense_by_month(account_admin, start_date, end_date)
    expense_category_labels, expense_category_data = get_expense_per_category(account_admin, start_date, end_date)
    return render(request, "fms/dashboard.html", {"total_income": total_income, "total_expense": total_expense, "current_balance": current_balance,
    "total_savings": total_savings, "selected_range": selected_range, "transactions":transactions, "labels": labels, "income_data":income_data, "expense_data": expense_data, "expense_category_labels":expense_category_labels,
                                                  "expense_category_data":expense_category_data, "budget_summaries":budget_summaries })

def view_analytics(request):
    account_admin = get_admin_user(request.user)

    selected_range = request.GET.get('range', 'month')
    range_func = RANGE_MAP.get(selected_range, get_this_month_range)
    start_date, end_date = range_func()

    total_expense = get_total_expense(account_admin, start_date, end_date)
    total_days = end_date - start_date
    average_daily_spend = round(float(total_expense / total_days.days),2)

    highest_expense = (Transaction.objects.filter(account_admin=account_admin, transaction_date__range=(start_date, end_date), transaction_type='EXP')
                       .values("transaction_date")
                       .annotate(total_spent=Sum("amount"))
                       .order_by("-transaction_date")
                       .first())
    if highest_expense:
        highest_spend_day = highest_expense['transaction_date']
        highest_spend_value = highest_expense['total_spent']
    else:
        highest_spend_day = "No expense"
        highest_spend_value = 0

    total_income = get_total_income(account_admin, start_date, end_date)
    total_expense = get_total_expense(account_admin, start_date, end_date)

    if total_income - total_expense == 0:
        savings_rate = 0
    else:
        savings_rate = round(((total_income - total_expense) / total_income) * 100, 2)

    most_used_category = get_most_used_category(account_admin, start_date, end_date)

    if not most_used_category:
        top_category = None
        top_category_amount = 0
    else:
        top_category = most_used_category['category__category_name']
        top_category_amount = most_used_category['total_amount']

    category_labels, category_data = get_expense_per_category(account_admin, start_date, end_date)

    if selected_range != 'year':
        m_spend_labels, m_spend_data = get_weekly_spend(account_admin, start_date, end_date)
    else:
        m_spend_labels, m_spend_data = get_monthly_spend(account_admin,start_date, end_date)

    alerts = get_alerts(account_admin)
    insight_messages = get_insights(account_admin, start_date, end_date)
    return render(request, "fms/analytics.html", {"selected_range": selected_range,"average_daily_spend":average_daily_spend,
                                                  "highest_spend_day":highest_spend_day,"highest_spend_value":highest_spend_value,
                                                  "top_category":top_category,"top_category_amount":top_category_amount,
                                                  "savings_rate":savings_rate,"m_spend_labels":m_spend_labels,
                                                  "m_spend_data":m_spend_data,"category_labels":category_labels,
                                                  "category_data":category_data, "alerts":alerts,
                                                  "insight_messages":insight_messages})
