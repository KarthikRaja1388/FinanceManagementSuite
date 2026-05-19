
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from category.models import Category


# Create your views here.
@login_required(login_url="login_page")
def view_category(request):

    user_profile = request.user.profile
    account_owner = request.user if user_profile.user_type == 'ADM' else user_profile.account_owner

    generic_categories = Category.objects.filter(user__isnull=True).order_by('category_name')
    user_categories = Category.objects.filter(user=account_owner).order_by('category_name')
    return render(request,'category/index.html', {"generic_categories":generic_categories, "user_categories": user_categories})

@login_required(login_url="login_page")
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        icon_class = request.POST.get('icon_class')
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
            icon_class = icon_class,
            user = account_owner,
        )

        messages.success(request, f"Category {category_name} added successfully")
        return redirect('view_category')

@login_required(login_url="login_page")
def update_category(request, category_id:int):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST' and category is not None:
        new_name = request.POST.get('category_name')
        new_icon = request.POST.get('icon_class')

        if not new_name:
            messages.info(request, "Category name can't be empty")
            return redirect("view_category")

        if new_name.isdigit():
            messages.info(request, "Category name is not valid")
            return redirect("view_category")

        category.category_name = new_name
        category.icon_class = new_icon
        category.save()

        messages.success(request, f'Category {new_name} is updated successfully')
        return redirect("view_category")

@login_required(login_url="login_page")
def delete_category(request, category_id:int):
    category = get_object_or_404(Category, id=category_id)

    try:
        if category is not None:
            category_name = category.category_name
            category.delete()
            messages.warning(request, f"Category {category_name} has been deleted!")
    except ValueError:
        messages.info(request, f'Unable to delete')
    except ProtectedError:
        messages.warning(request,
                         f"Cannot delete '{category.category_name}' because it contains active sub-categories.\n"
                         "Please delete or move the sub-categories first. ")
    return redirect('view_category')


