from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.view_transactions, name='view_transactions'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('update/<int:transaction_id>', views.update_transaction, name='update_transaction'),
    path('delete/<int:transaction_id>', views.delete_transaction, name='delete_transaction'),
]
