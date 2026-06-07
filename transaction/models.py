from django.db import models
from django.conf import settings
from django.utils.timezone import now

from account.models import Account
from category.models import Category


# Create your models here.
class Transaction(models.Model):

    class TransactionType(models.TextChoices):
        INCOME = 'INC'
        EXPENSE = 'EXP'

    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    description = models.TextField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='category')
    transaction_type = models.CharField(max_length=3, choices=TransactionType.choices)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='txn_user')
    account_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='account_admin')
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    transaction_date = models.DateField(default=now)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.transaction_type

