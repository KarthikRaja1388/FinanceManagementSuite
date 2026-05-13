from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_category, name="view_category"),
    path("/add", views.add_category, name="add_category"),
]