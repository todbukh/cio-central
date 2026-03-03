from django.shortcuts import render, redirect


# Create your views here.
def home(request):
    if not request.user.is_authenticated: return redirect("/accounts/login/")

    context = {
        "authenticated": True,
        "user": request.user
    }

    return render(request, "core/index.html", context)