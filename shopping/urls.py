from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_shoppinglist, name="view_shopping_list"),
    path("add/", views.add_shoppinglist, name="add_shopping_list"),
    path("update/<int:shopping_list_id>", views.update_shoppinglist, name="update_shopping_list"),
    path("complete/<int:shopping_list_id>", views.complete_shoppinglist, name="complete_shopping_list"),
    path("shoppingitems/", views.view_shopping_items, name="view_shopping_items"),
    path("<int:shopping_list_id>/shoppingitems/add", views.add_shopping_item, name="add_shopping_item"),
    path("shoppingitems/update/<int:shopping_item_id>", views.update_shopping_item, name="update_shopping_item"),
    path("shoppingitems/togglepurchased/<int:shopping_item_id>", views.toggle_item_purchased, name="toggle_item_purchased"),
    path("shoppingitems/delete/<int:shopping_item_id>", views.delete_item, name="delete_item"),

]