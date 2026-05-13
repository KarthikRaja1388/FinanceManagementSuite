
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from category.models import Category
from identity.models import UserProfile


# Create your views here.
def view_category(request):
    return render(request,'category/index.html')

@login_required(login_url="login_page")
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        current_user_profile = request.user.profile

        if current_user_profile.user_type == 'ADM':
            account_owner = request.user
        else:
            account_owner = current_user_profile.account_owner

        if not category_name:
            messages.info(request, "Category name can't be empty")
            return redirect("view_category")

        if category_name.isdigit():
            messages.info(request, "Category name is not valid")
            return redirect("view_category")

        Category.objects.create(
            category_name = category_name,
            user = account_owner,
        )

        messages.success(request, f"Category {category_name} added successfully")
        return redirect('view_category')
