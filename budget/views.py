from sys import is_stack_trampoline_active

from django.contrib.auth.decorators import login_required
from django.db.models import Q, DecimalField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from budget.models import Budget
from budget.utils import get_spent_amount, get_budget_percentage_used, get_budget_remaining_amount
from category.models import Category
from identity.utils import get_admin_user
from transaction.models import Transaction


@login_required(login_url="login_page")
def view_budget(request):

    budgets = Budget.objects.filter(added_by = get_admin_user(request.user), is_active=True)
    categories = Category.objects.filter(Q(user= get_admin_user(request.user)) | Q(user__isnull=True))
    for budget in budgets:

        budget.spent_amount = get_spent_amount(
            get_admin_user(request.user),
            budget.start_date,
            budget.end_date,
            budget.category
        )
        budget.percentage_used = get_budget_percentage_used(
                            budget.budget_amount,
                            budget.spent_amount)
        budget.remaining_amount = get_budget_remaining_amount(budget.budget_amount, budget.spent_amount)

    return render(request, "budget/index.html", {"budgets":budgets, "categories":categories})

@login_required(login_url="login_page")
def add_budget(request):
    if request.method == 'POST':
        budget_name = request.POST.get('budget_name')
        period = request.POST.get('period')
        budget_amount = request.POST.get('budget_amount')
        budget_category = request.POST.get('budget_category')
        budget_type = request.POST.get('budget_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        fields = {
            "Budget Name": budget_name,
            "Budget Amount": budget_amount,
            "Budget Type": budget_type,
            "Period": period,
            "Start Date": start_date,
            "End Date": end_date,
        }

        missing_fields = [
            field_name
            for field_name, value in fields.items()
            if not value
        ]

        if missing_fields:
            messages.warning(request,f"Required fields missing: {', '.join(missing_fields)}")
            return redirect("view_budget")

        if not budget_amount.isdecimal():
            messages.warning(request,"Enter a valid budget amount")
            return redirect("view_budget")

        if float(budget_amount) <= 0:
            messages.warning(request, "Budget amount can't be zero")
            return redirect("view_budget")

        try:
            Budget.objects.create(
                budget_name=budget_name,
                period=period,
                budget_type = budget_type,
                budget_amount = budget_amount,
                category = budget_category,
                added_by = get_admin_user(request.user),
                start_date = start_date,
                end_date = end_date
            )
            messages.success(request, "Budget added successfully!")
            return redirect('view_budget')
        except Exception as e:
            messages.warning(request, f"Unable to add Budget: {e}")
            return redirect('view_budget')

@login_required(login_url="login_page")
def update_budget(request, budget_id:int):
    budget_for_id = get_object_or_404(Budget, id=budget_id, added_by=get_admin_user(request.user))
    if request.method == 'POST':
        new_budget_name = request.POST.get('budget_name')
        new_period = request.POST.get('period')
        new_budget_type = request.POST.get('budget_type')
        new_budget_amount = request.POST.get('budget_amount')
        new_budget_category = request.POST.get('budget_category')
        new_start_date = request.POST.get('start_date')
        new_end_date = request.POST.get('end_date')

        print(new_start_date, new_end_date, new_budget_name, new_budget_amount)
        fields = {
            "Budget Name": new_budget_name,
            "Budget Amount": new_budget_amount,
            "Budget Type": new_budget_type,
            "Period": new_period,
            "Start Date": new_start_date,
            "End Date": new_end_date,
        }

        missing_fields = [
            field_name
            for field_name, value in fields.items()
            if not value
        ]

        if missing_fields:
            messages.warning(request, f"Required fields missing: {', '.join(missing_fields)}")
            return redirect("view_budget")

        if new_start_date >= new_end_date:
            messages.warning(request, "Start date can't be greater than end date")
            return redirect("view_budget")

        try:
            budget_for_id.budget_name = new_budget_name
            budget_for_id.budget_amount = new_budget_amount
            budget_for_id.budget_type = new_budget_type
            budget_for_id.category = new_budget_category
            budget_for_id.period = new_period
            budget_for_id.start_date = new_start_date
            budget_for_id.end_date = new_end_date

            budget_for_id.save()
            messages.success(request, "Budget has been updated successfully!")
            return redirect("view_budget")

        except Exception as e:
            messages.warning(request, "Unable to update the budget")
            return redirect("view_budget")

def disable_budget(request, budget_id:int):
    budget_for_id = get_object_or_404(Budget, id=budget_id, added_by=get_admin_user(request.user))
    print(budget_for_id)
    budget_name = budget_for_id.budget_name
    budget_for_id.is_active = False
    budget_for_id.save()
    messages.info(request,f"Budget {budget_name} has been disabled")
    return redirect("view_budget")


