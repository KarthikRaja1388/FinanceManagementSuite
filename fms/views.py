from django.shortcuts import render


def view_dashboard(request):
    return render(request, "fms/dashboard.html")