
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', views.view_dashboard, name="view_dashboard"),
    path("", include('identity.urls')),
    path("category/", include('category.urls')),
    path('account/', include('account.urls')),
    path('transaction/', include('transaction.urls')),
    path('budget/', include('budget.urls')),
]
