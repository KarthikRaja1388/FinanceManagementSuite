from itertools import count

from django.db.models import Sum

from budget.models import Budget
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

def get_alerts(user):
    active_budgets = (Budget.objects.filter(added_by=user, is_active=True))

    alerts = []
    for budget in active_budgets:
        expense = get_spent_amount(user, budget.start_date, budget.end_date, budget.category)

        budget_percent_used = get_budget_percentage_used(budget.budget_amount, expense)

        if budget_percent_used >= 100:
            exceeded_by = expense - budget.budget_amount
            alerts.append({
                "message": (
                    f" You have exceeded your <b>{budget.budget_name} budget</b> by <b>{exceeded_by}</b>. Review your recent spending to stay on track." ),
                "alert_type":"negative"
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

    if most_used_category:
        insights.append({
            "message": f"{most_used_category['category__category_name']} was your most frequent purchase category with {most_used_category['used']} transactions."
        })

    return insights