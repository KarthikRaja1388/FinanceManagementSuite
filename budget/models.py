from django.db import models

from category.models import Category
from django.conf import settings


# Create your models here.
class Budget(models.Model):

    class BudgetPeriod(models.TextChoices):
        WEEKLY = 'weekly'
        FORTNIGHTLY = 'fortnightly'
        MONTHLY = 'monthly'
        YEARLY = 'yearly'

    budget_name = models.CharField(max_length=100)
    period = models.CharField(max_length=11, choices=BudgetPeriod.choices)
    budget_amount = models.DecimalField(max_digits=10, decimal_places=2)
    budget_type = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='budget_user')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.budget_name} - {self.budget_amount}"

