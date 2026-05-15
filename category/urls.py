from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_category, name="view_category"),
    path("add", views.add_category, name="add_category"),
    path("update/<int:category_id>", views.update_category, name="update_category"),
    path("delete/<int:category_id>", views.delete_category, name="delete_category"),

]