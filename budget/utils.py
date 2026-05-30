from django.db.models import Sum

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

