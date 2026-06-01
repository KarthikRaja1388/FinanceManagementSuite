from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.aggregates import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from category.models import Category
from identity.utils import get_admin_user
from shopping.models import ShoppingList, ShoppingItem


@login_required(login_url="login_page")
def view_shoppinglist(request):
    categories = Category.objects.filter(Q(user=get_admin_user(request.user)) | Q(user__isnull=True))
    shopping_lists = ShoppingList.objects.filter(user=get_admin_user(request.user), completed=False)
    return render(request,"shopping/index.html", {"categories": categories, "shopping_lists":shopping_lists})

@login_required(login_url="login_page")
def add_shoppinglist(request):
    if request.method == 'POST':
        list_name = request.POST.get('list_name')
        category = request.POST.get('category')

        category_obj = get_object_or_404(Category, id=category)

        if not list_name:
            messages.warning(request,"List name can't be empty")
            return redirect("view_shopping_list")

        if not category:
            messages.warning(request, "Category can't be empty")
            return redirect("view_shopping_list")

        ShoppingList.objects.create(
            list_name=list_name,
            user=get_admin_user(request.user),
            category=category_obj
        )
        messages.success(request,"Shopping List has been added successfully")
        return redirect("view_shopping_list")

@login_required(login_url="login_page")
def update_shoppinglist(request, shoppinglist_id:int):
    shoppinglist_obj = get_object_or_404(ShoppingList, id=shoppinglist_id)

    if request.method == 'POST':
        new_list_name = request.POST.get('list_name')
        new_category_id = request.POST.get('category')

        if not new_list_name:
            messages.warning(request,"List name can't be empty")
            return redirect("view_shopping_list")

        if not new_category_id:
            messages.warning(request, "Category can't be empty")
            return redirect("view_shopping_list")

        try:
            shoppinglist_obj.list_name = new_list_name
            shoppinglist_obj.category_id = new_category_id
            shoppinglist_obj.save()
            messages.success(request, "Shopping list has been updated successfully!")
            return redirect("view_shopping_list")
        except Exception as e:
            raise e

@login_required(login_url="login_page")
def complete_shoppinglist(request, shopping_list_id:int):
    shoppinglist_obj = get_object_or_404(ShoppingList, id=shopping_list_id)
    amount_spent = ShoppingList.objects.select_related("items").aggregate(amount_spent=Sum('item_price'))

    shoppinglist_obj.total_spent = amount_spent
    shoppinglist_obj.completed = True
    shoppinglist_obj.completed_at = timezone.now()
    shoppinglist_obj.save()

    messages.success(request, "Shopping list has been marked as complete!")
    return redirect("view_shopping_list")

# shopping items
@login_required(login_url="login_page")
def view_shopping_items(request):
    shoppinglist_obj = get_object_or_404(ShoppingList, user= get_admin_user(request.user), completed=False)
    shopping_items = ShoppingItem.objects.filter(shopping_list=shoppinglist_obj)
    total_items = shopping_items.count()
    purchased_count = shopping_items.filter(purchased=True).count()
    completion_percentage = ( round((purchased_count/total_items)*100) if total_items > 0 else 0)
    total_price = sum(
        item.item_price * item.quantity
        for item in shopping_items
    )
    return render(request, "shopping/shoppingitems.html", {"shopping_list": shoppinglist_obj, "shopping_items": shopping_items, "total_items":total_items, "purchased_count":purchased_count,"completion_percentage":completion_percentage, "total_price": total_price})

@login_required(login_url="login_page")
def add_shopping_item(request, shopping_list_id:int):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        quantity = request.POST.get('quantity')
        item_price = request.POST.get('item_price')

        if not item_name:
            messages.warning(request, "Item name can't be empty")
            return redirect("view_shopping_items")

        item_price = float(item_price or 0)

        shopping_list_related = get_object_or_404(ShoppingList, id=shopping_list_id)
        try:
            ShoppingItem.objects.create(
                item_name = item_name,
                item_price = item_price,
                quantity = quantity,
                shopping_list = shopping_list_related
            )
            messages.success(request, "Item added successfully to the list!")
            return redirect("view_shopping_items")
        except Exception as e:
            raise e

@login_required(login_url="login_page")
def update_shopping_item(request, shopping_item_id:int):

    shopping_item_obj = get_object_or_404(ShoppingItem, id=shopping_item_id)

    if request.method == 'POST':
        new_item_name = request.POST.get('item_name')
        new_quantity = request.POST.get('quantity')
        new_item_price = request.POST.get('item_price')

        if not new_item_name:
            messages.warning(request, "Item name can't be empty")
            return redirect("view_shopping_items")

        if new_item_price:
            new_item_price = float(new_item_price)
        else:
            new_item_price = float(0)

        shopping_item_obj.item_name = new_item_name
        shopping_item_obj.quantity = new_quantity
        shopping_item_obj.item_price = new_item_price
        shopping_item_obj.save()

        messages.success(request, "Item has been updated successfully!")
        return redirect("view_shopping_items" )

@login_required(login_url="login_page")
def toggle_item_purchased(request, shopping_item_id:int):
    item = get_object_or_404(ShoppingItem, id=shopping_item_id)
    item.purchased = not item.purchased
    item.save()
    return redirect("view_shopping_items")

@login_required(login_url="login_page")
def delete_item(request, shopping_item_id:int):
    item = get_object_or_404(ShoppingItem, id=shopping_item_id)
    item.delete()
    messages.warning(request, "Item has been deleted!")
    return redirect("view_shopping_items")
