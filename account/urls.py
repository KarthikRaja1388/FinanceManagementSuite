from django.urls import path

from . import views

urlpatterns = [
    path("", views.view_account, name='view_account'),
    path("add/",views.add_account,name='add_account' ),
    path("update/<int:account_id>", views.update_account, name='update_account'),
    path("delete/<int:account_id>", views.delete_account, name='delete_account'),
]