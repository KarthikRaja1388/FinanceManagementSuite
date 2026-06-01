from django.conf import settings
from django.db import models

from category.models import Category


class ShoppingList(models.Model):
    list_name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="shopping_lists")
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.list_name


class ShoppingItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name="items")
    item_name = models.CharField(max_length=100)
    item_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=1)
    purchased = models.BooleanField(default=False)

    class Meta:
        ordering = ['purchased', 'id']

    def __str__(self):
        return self.item_name