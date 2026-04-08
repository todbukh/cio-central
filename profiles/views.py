from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import ProfileEditForm
from django.core.files.storage import default_storage

User = get_user_model()

@login_required(login_url="/login/")
def profile_redirect(request):
    return redirect("profiles:profile", username=request.user.username)

@login_required(login_url="/login/")
def profile_view(request, username):
    if request.user.is_user_admin(): raise Http404

    profile_user = get_object_or_404(User, username=username)
    is_owner =  request.user == profile_user
    context = {
        "profile_user": profile_user,
        "is_owner": is_owner
    }
    return render(request, "profiles/profile.html", context)

@login_required(login_url="/login/")
def profile_edit_view(request, username):
    if request.user.username != username: # only allow users to edit their own profile
        return redirect("profiles:profile", username=username)

    profile = request.user.profile

    if request.method == "POST": # user wants to save changes to profile
        if "delete_picture" in request.POST: # user clicks delete button to clear profile picture
            if profile.profile_picture:
                profile.profile_picture.delete()
            return redirect("profiles:profile", username = username)
        profile_picture_file_name = None
        if 'profile_picture' in request.FILES and profile.profile_picture:
            profile_picture_file_name = profile.profile_picture.name # use of .name to pass in string

        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if profile_picture_file_name: default_storage.delete(profile_picture_file_name)
            form.save()
            return redirect("profiles:profile", username=username)
    else:                       # user just wants to view the edit page
        form = ProfileEditForm(instance=profile)

    return render(request, "profiles/profile_edit.html", {"form": form, "profile_user": request.user})
