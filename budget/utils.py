from django.utils import timezone

from django.db.models import Sum

from budget.models import Budget
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

        if budget.budget_amount <= expense:
            exceeded_by = expense - budget.budget_amount
            alerts.append({
                "message": (
                    f"Budget <b>{budget.budget_name}</b> exceeded by <b>{exceeded_by}</b> "
                    f"(limit: {budget.budget_amount})"
                ),
                "alert_type":"negative"
            })
    return alerts
