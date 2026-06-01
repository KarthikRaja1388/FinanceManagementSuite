from django.contrib import admin

from shopping.models import ShoppingList, ShoppingItem

# Register your models here.
admin.site.register(ShoppingList)
admin.site.register(ShoppingItem)