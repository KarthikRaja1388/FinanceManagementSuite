from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="login_page"),
    path("signup", views.signup_user, name="signup_user"),
    path("authenticate", views.authenticate_user, name="authenticate_user"),
    path("logout", views.logout_user, name="logout_user"),
]
