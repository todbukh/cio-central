from django.shortcuts import render, redirect
# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    return render(request, "core/login.html")