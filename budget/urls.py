from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_budget, name="view_budget"),
    path("add/", views.add_budget, name="add_budget"),
    path("update/<int:budget_id>", views.update_budget, name="update_budget"),
    path("disable/<int:budget_id>", views.disable_budget, name="disable_budget"),
]