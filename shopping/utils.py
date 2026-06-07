from collections import defaultdict

from django.db.models.aggregates import Count, Sum
from django.db.models.functions import TruncWeek, TruncMonth

from transaction.models import Transaction


def get_total_amount_spent(items):

    total_spent=0
    for item in items:
        total_price = item.total_price
        total_spent += total_price
    return total_spent

def get_most_used_category(user, start_date, end_date):
    transaction = (Transaction.objects.filter(account_admin=user,transaction_date__range=(start_date, end_date), transaction_type="EXP")
                   .values('category__category_name')
                   .annotate(used=Count('id'), total_amount=Sum('amount'))
                   .order_by('-total_amount')
                   .first()
                   )
    return transaction

def get_weekly_spend(user, start_date, end_date):
    weekly_spend = (
        Transaction.objects.filter(
            account_admin=user,
            transaction_date__range=(start_date, end_date),
            transaction_type="EXP"
        )
        .annotate(week=TruncWeek('transaction_date'))
        .values('week')
        .annotate(sp_amount=Sum('amount'))
        .order_by('week')
    )

    spend_labels = [
        item['week'].strftime('Week %d %b')
        for item in weekly_spend
    ]

    spent_amount = [
        int(item['sp_amount'])
        for item in weekly_spend
    ]

    return spend_labels, spent_amount

def get_monthly_spend(user, start_date, end_date):
    monthly_spend = (Transaction.objects.filter(
            account_admin=user,
            transaction_date__range=(start_date, end_date),
            transaction_type="EXP"
        ).annotate(month=TruncMonth('transaction_date'))
                     .values('month')
                     .annotate(sp_amount=Sum('amount'))
                     .order_by('month'))
    spend_labels = [
        item['month'].strftime('%b')
        for item in monthly_spend
    ]

    spend_amount = [
        int(item['sp_amount'])
        for item in monthly_spend
    ]

    return spend_labels, spend_amount

