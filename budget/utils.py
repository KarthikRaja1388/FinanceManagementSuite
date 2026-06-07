from django.db.models import Sum, Avg
from django.db.models.functions import TruncMonth

from budget.models import Budget
from category.models import Category
from shopping.utils import get_most_used_category
from transaction.models import Transaction


def get_spent_amount(user, start_date, end_date, category=None):

    filters = {
        'account_admin': user,
        'transaction_type': 'EXP',
        'transaction_date__range': (start_date, end_date)
    }

    if category is not None:
        filters['category_id'] = category.id

    return (
        Transaction.objects.filter(**filters)
        .aggregate(total=Sum('amount'))['total'] or 0
    )

def get_budget_percentage_used(budget_amount, spent_amount):
    if not budget_amount:
        return 0
    return round((spent_amount/budget_amount)*100,2)

def get_budget_remaining_amount(budget_amount, spent_amount):
    return budget_amount - spent_amount

def get_avg_monthly_spend(user, start_date, end_date):
    monthly_spend = (Transaction.objects.filter(account_admin=user, transaction_date__range=(start_date, end_date),transaction_type='EXP')
                     .annotate(spend_month=TruncMonth('transaction_date'))
                     .values('spend_month')
                     .annotate(total_spend=Sum('amount'))
                     .order_by('spend_month'))
    avg_spend = monthly_spend.aggregate(avg_spend=(Avg('total_spend')))['avg_spend']
    if avg_spend is not None:
        avg_spend = round(avg_spend,2)
    else:
        avg_spend = 0
    return avg_spend

def get_spend_comparison_previous_period(user, start_date, end_date):
    pass

from django.db.models import Sum

def get_highest_category_spend_percentage(user, start_date, end_date):
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

    if not expense_per_category:
        return None

    total_spend = sum(item['total_amount'] for item in expense_per_category)

    top_category = expense_per_category[0]

    category = Category.objects.get(id=top_category['category'])

    percentage = round(
        (top_category['total_amount'] / total_spend) * 100
    )

    return {
        'category_name': category.category_name,
        'amount': top_category['total_amount'],
        'percentage': percentage
    }

def get_alerts(user):
    active_budgets = (Budget.objects.filter(added_by=user, is_active=True))

    alerts = []
    for budget in active_budgets:
        expense = get_spent_amount(user, budget.start_date, budget.end_date, budget.category)

        budget_percent_used = get_budget_percentage_used(budget.budget_amount, expense)

        if budget_percent_used > 100:
            exceeded_by = expense - budget.budget_amount
            alerts.append({
                "message": (
                    f" You have exceeded your <b>{budget.budget_name} budget</b> by <b>{exceeded_by}</b>. Review your recent spending to stay on track." ),
                "alert_type":"danger"
            })
        elif budget_percent_used == 100:
            alerts.append({
                "message": (
                    f" You have reached your <b>{budget.budget_name} budget limit</b>. It might be a good time to review your spending."),
                "alert_type": "danger"
            })
        elif budget_percent_used >= 80:
            alerts.append({
                "message": (f"You have used 80% of your {budget.budget_name} budget. Keep an eye for the rest of the period."),
                "alert_type": "warning"
            })
    return alerts

def get_insights(user, start_date, end_date):
    insights = []

    most_used_category = get_most_used_category(user, start_date, end_date)
    avg_spend = get_avg_monthly_spend(user, start_date, end_date)
    highest_category_spend_percentage= get_highest_category_spend_percentage(user, start_date, end_date)

    if most_used_category:
        insights.append({
            "message": (f"<b>{most_used_category['category__category_name']}</b> was your most frequent purchase category for the selected period, with <b>{most_used_category['used']}</b> transactions totaling <b>${most_used_category['total_amount']}</b>.")
        })

    if avg_spend:
        insights.append({
            "message":(f"Your typical monthly spending was around <b>${avg_spend}</b> over the selected period. Use this as a benchmark when setting future budgets.")
        })

    if highest_category_spend_percentage:
        insights.append({
            "message": (
                f"<b>{highest_category_spend_percentage['category_name']}</b> accounts for <b>{highest_category_spend_percentage['percentage']}%</b> of your total spending for the selected period.")
        })
    return insights

