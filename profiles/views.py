from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from .forms import ProfileEditForm

User = get_user_model()

# used to check if user is approved before allowing access to profile pages
# unapproved users shouldn't be able to see profiles
def is_approved(user):
    return not user.is_anonymous and user.status == "APPROVED"

@login_required(login_url="/login/")
@user_passes_test(is_approved, login_url="/", redirect_field_name=None)
def profile_redirect(request):
    return redirect("profiles:profile", username=request.user.username)

@login_required(login_url="/login/")
@user_passes_test(is_approved, login_url="/", redirect_field_name=None)
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_owner =  request.user == profile_user
    context = {
        "profile_user": profile_user,
        "is_owner": is_owner,
    }
    return render(request, "profiles/profile.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_approved, login_url="/", redirect_field_name=None)
def profile_edit_view(request, username):
    if request.user.username != username: # only allow users to edit their own profile
        return redirect("profiles:profile", username=username)

    profile = request.user.profile

    if request.method == "POST": # user wants to save changes to profile
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profiles:profile", username=username)
    else:                       # user just wants to view the edit page
        form = ProfileEditForm(instance=profile)

    return render(request, "profiles/profile_edit.html", {"form": form})
