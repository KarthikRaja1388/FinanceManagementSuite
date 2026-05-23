from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from category.models import Category
from transaction.models import Transaction


@login_required(login_url="login_page")
def view_transactions(request):
    user_profile = request.user.profile
    if user_profile.user_type == 'ADM':
        account_admin = request.user
    else:
        account_admin = user_profile.account_owner

    transactions = Transaction.objects.filter(account_admin = account_admin)
    categories = Category.objects.filter(Q(user=account_admin) | Q(user__isnull = True))

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category_id = request.GET.get('category')
    transaction_type = request.GET.get('transaction_type')

    print(f"start date {start_date}")

    if start_date:
        transactions = transactions.filter(transaction_date__gte=start_date)

    if end_date:
        transactions = transactions.filter(transaction_date__lte=end_date)

    if category_id:
        transactions = transactions.filter(category=category_id)

    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)

    transactions = transactions.order_by('-transaction_date')

    return render(request, 'transaction/index.html', {"transactions": transactions, "categories": categories})

@login_required(login_url="login_page")
def add_transaction(request):

    if request.method == 'POST':
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        transaction_type = request.POST.get('transaction_type')
        category_id = request.POST.get('category')
        transaction_date = request.POST.get('transaction_date')

        fields = {
            "Description": description,
            "Amount": amount,
            "Transaction Type": transaction_type,
            "Category": category_id,
            "Transaction Date": transaction_date,
        }

        missing_fields = [
            field_name
            for field_name, value in fields.items()
            if not value
        ]

        if missing_fields:
            messages.warning(
                request,
                f"Required fields missing: {', '.join(missing_fields)}"
            )
            return redirect('view_transactions')

        added_by = request.user
        user_profile = request.user.profile

        if user_profile.user_type == 'ADM':
            account_admin = added_by
        else:
            account_admin = user_profile.account_owner

        try:
            category_obj = get_object_or_404(Category, id=category_id)

            Transaction.objects.create(
                description = description,
                amount = amount,
                category = category_obj,
                transaction_type = transaction_type,
                added_by = request.user,
                account_admin = account_admin,
                transaction_date = transaction_date,
            )
            messages.success(request, "Transaction added successfully!")
        except Exception as e:
            messages.warning(request, "Unable to add transaction")
        return redirect('view_transactions')

@login_required(login_url="login_page")
def update_transaction(request, transaction_id:int):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if request.method == 'POST':
        new_description = request.POST.get('description')
        new_amount = request.POST.get('amount')
        new_transaction_type = request.POST.get('transaction_type')
        new_category_id = request.POST.get('category_id')
        new_transaction_date = request.POST.get('transaction_date')

        try:
            new_category_obj = get_object_or_404(Category, id=new_category_id)
            transaction.description = new_description
            transaction.amount = new_amount
            transaction.transaction_type = new_transaction_type
            transaction.category = new_category_obj
            transaction.transaction_date = new_transaction_date
            transaction.save()
            messages.success(request, "Transaction updated successfully")
        except Exception as e:
            messages.warning(request, f'Failed to update Transaction:{e}')
    return redirect('view_transactions')

def delete_transaction(request, transaction_id:int):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    try:
        if transaction is not None:
            transaction.delete()
            messages.info(request, "Transaction has been deleted!")
    except Exception:
        messages.warning(request,"Unable to delete Transaction")

    return redirect('view_transactions')



