from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def profile_redirect(request):
    return redirect("profiles:profile", username=request.user.username)

def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_owner = request.user.is_authenticated and request.user == profile_user
    context = {
        "profile_user": profile_user,
        "is_owner": is_owner,
    }
    return render(request, "profiles/profile.html", context)
