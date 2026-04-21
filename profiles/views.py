from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from django.views.decorators.http import require_POST

from core.permissions import is_executive, is_owner

from .forms import ProfileEditForm
from django.core.files.storage import default_storage

User = get_user_model()

def can_delete(user, profile_user):
    if profile_user.role != User.Role.USERADMIN:
        if profile_user.status == User.Status.DELETED:
            return False
        if is_owner(user):
            return True
        if is_executive(user) and not is_executive(profile_user):
            return True
        if user == profile_user:
            return True
    return False

@login_required(login_url="/login/")
def profile_redirect(request):
    return redirect("profiles:profile", username=request.user.username)

@login_required(login_url="/login/")
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    if profile_user.status != "APPROVED" or profile_user.role == User.Role.USERADMIN:
        raise Http404
    user_is_profile_owner =  request.user == profile_user
    context = {
        "profile_user": profile_user,
        "is_executive": is_executive(request.user),
        "user_is_profile_owner": user_is_profile_owner,
        "can_delete": can_delete(request.user, profile_user)
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
            if profile_picture_file_name:
                default_storage.delete(profile_picture_file_name)

            profile = form.save()

            request.user.first_name = form.cleaned_data["first_name"]
            request.user.last_name = form.cleaned_data["last_name"]
            request.user.save()

            return redirect("profiles:profile", username=username)

    else:                       # user just wants to view the edit page

        # prefill the form with the user's current name because first and last name live on User
        form = ProfileEditForm(instance=profile,
            initial={"first_name": request.user.first_name, "last_name": request.user.last_name,}
        )

    return render(request, "profiles/profile_edit.html", {"form": form, "profile_user": request.user})

@require_POST
@login_required
def delete_user(request, username):
    member = get_object_or_404(User, username=username)

    if not can_delete(request.user, member):
        return HttpResponseForbidden()

    member.is_active = False
    member.save()

    if request.user == member:
        logout(request)

    member.delete()
    return redirect("/")
