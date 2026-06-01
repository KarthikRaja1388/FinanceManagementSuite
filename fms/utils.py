from collections import defaultdict
from datetime import timedelta

from django.db.models import Q, Sum
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta

from account.models import Account
from budget.models import Budget
from budget.utils import get_spent_amount
from category.models import Category
from transaction.models import Transaction

def get_current_balance(user):
    account = Account.objects.filter(
        account_admin=user,
        is_primary=True
    ).first()
    return account.current_balance if account else 0


def get_total_income(user, start, end):
    return Transaction.objects.filter(
        account_admin=user,
        transaction_type="INC",
        transaction_date__range=[start, end]
    ).aggregate(total=Sum('amount'))['total'] or 0

def get_total_expense(user, start,end):
    return Transaction.objects.filter(
        account_admin=user,
        transaction_type="EXP",
        transaction_date__range=[start, end]
    ).aggregate(total=Sum('amount'))['total'] or 0

def get_total_savings(user, start,end):
    savings = get_total_income(user, start, end) - get_total_expense(user, start,end)
    return savings

def get_this_week_range():
    today = now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    return week_start,week_end

def get_last_week_range():
    today = now().date()
    current_week_start = today - timedelta(days=today.weekday())
    week_start = current_week_start - timedelta(days=7)
    week_end =  current_week_start - timedelta(days=1)
    return  week_start, week_end

def get_this_month_range():
    today = now().date()
    current_month_start = today.replace(day=1)
    return current_month_start, today

def get_last_3_months_range():
    today = now().date()
    range_start = today - relativedelta(months=3)
    return range_start, today

def get_this_year_range():
    today = now().date()
    current_year_start = today.replace(month=1, day=1)
    return current_year_start, today

def get_income_expense_by_month(user,start_date, end_date):
    income_by_month = (
        Transaction.objects.filter(
            account_admin= user,
            transaction_type = "INC",
            transaction_date__range=[start_date, end_date]
        )
        .annotate(month=TruncMonth('transaction_date'))
        .values('month')
        .annotate(total=Sum('amount'))
    )

    expense_by_month = (
        Transaction.objects.filter(
            account_admin=user,
            transaction_type="EXP",
            transaction_date__range=[start_date, end_date]
        )
        .annotate(month=TruncMonth('transaction_date'))
        .values('month')
        .annotate(total=Sum('amount'))
    )

    income_map = defaultdict(float)
    expense_map = defaultdict(float)


    for item in income_by_month:
        income_map[item['month']] = float(item['total'])

    for item in expense_by_month:
        expense_map[item['month']] = float(item['total'])

    all_months = sorted(set(income_map.keys()) | set(expense_map.keys()))

    labels = [m.strftime('%b %Y') for m in all_months]
    income = [income_map[m] for m in all_months]
    expense = [expense_map[m] for m in all_months]

    return labels, income, expense

def get_expense_per_category(user, start_date, end_date):
    expense_per_category = (
        Transaction.objects.filter(
            account_admin=user,
            transaction_type="EXP",
            transaction_date__range=[start_date, end_date]
        )
        .values('category')
        .annotate(total_amount=Sum('amount'))
        .order_by('-total_amount')
    )

    category_ids = [item['category'] for item in expense_per_category]

    categories = Category.objects.in_bulk(category_ids)

    labels = [
        categories[item['category']].category_name
        for item in expense_per_category
        if item['category'] in categories
    ]

    data = [
        float(item['total_amount'])
        for item in expense_per_category
    ]
    return  labels, data

def get_budget_summary(user):
    budget_summary = []

    budgets = Budget.objects.filter(
        added_by = user,
        is_active = True,
        category__isnull = False
    ).select_related('category')
    for budget in budgets:
        spent_amount = get_spent_amount(user, budget.start_date, budget.end_date, budget.category)
        percentage_used =(round((spent_amount/budget.budget_amount)*100,2) if budget.budget_amount > 0 else 0)
        budget_summary.append({
            "label": budget.category.category_name,
            "spent_amount":spent_amount,
            "budget_amount":budget.budget_amount,
            "percentage_used":percentage_used

        })
    return budget_summary
