from django.contrib.admin.actions import delete_selected
from django.contrib.auth import user_logged_in
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from account.models import Account


@login_required(login_url="login_page")
def view_account(request):
    accounts = Account.objects.filter(account_admin=request.user)
    return render(request, "account/index.html", {"accounts": accounts})

@login_required(login_url="login_page")
def add_account(request):
    if request.method == "POST":
        account_name = request.POST.get('account_name')
        current_balance = request.POST.get('current_balance')
        is_primary_raw = request.POST.get('is_primary')
        user_profile = request.user.profile

        is_primary = is_primary_raw == 'on'

        if not account_name:
            messages.warning(request, "Account name can't be empty")
            return redirect("view_account")

        if account_name.isdigit():
            messages.info(request, "Account name is not valid")
            return redirect("view_account")

        if user_profile.user_type != 'ADM':
            messages.info(request, "You do not have permission to add an account!")
            return redirect("view_account")

        try:
            Account.objects.create(
                account_name = account_name,
                current_balance = current_balance,
                account_admin = request.user,
                is_primary = is_primary,
            )
            messages.success(request, f"Account {account_name} added successfully")
            return redirect("view_account")
        except ValueError as e:
            messages.info(request, "Unable to add account")

            return redirect("view_account")

@login_required(login_url="login_page")
def update_account(request, account_id:int):
    account = get_object_or_404(Account, id=account_id)

    if request.method == 'POST' and account is not None:
        new_account_name = request.POST.get('account_name')
        new_balance = request.POST.get('current_balance')
        new_is_primary = request.POST.get('is_primary') == 'on'

        if not new_account_name:
            messages.warning(request, "Account name can't be empty")
            return redirect("view_account")

        if new_account_name.isdigit():
            messages.info(request, "Account name is not valid")
            return redirect("view_account")

        if new_is_primary:
            Account.objects.filter(account_admin = request.user, is_primary = True).update(is_primary=False)

        account.account_name = new_account_name
        account.current_balance = new_balance
        account.is_primary = new_is_primary

        account.save()
        messages.info(request, "Account has been updated successfully!")
        return redirect("view_account")

@login_required(login_url="login_page")
def delete_account(request, account_id:int):
    account = get_object_or_404(Account, id=account_id)

    try:
        if account is not None:
            account_name = account.account_name
            account.delete()
            messages.success(request, f"Account {account_name} has been deleted!")
            return redirect("view_account")
    except ProtectedError:
        messages.warning(request,"This account cannot be deleted because it has linked transactions.")
    return redirect("view_account")






