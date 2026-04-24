from django.core.files.storage import default_storage
from django.shortcuts import render, redirect

from core.decorators import owner_required
from organization_edit.forms import OrganizationEditForm
from organization_edit.models import Organization


# Create your views here.
@owner_required(redirect_url="organization:home")
def index(request):
    organization, created = Organization.objects.get_or_create(
        id=0
    )

    context = {
        "active_tab": "organization-edit",
        "organization": organization,
    }

    return render(request, "organization_edit/index.html", context)

@owner_required(redirect_url="organization:home")
def edit(request):
    organization, created = Organization.objects.get_or_create(
        id=0
    )

    if request.method == "POST":
        if "delete_picture" in request.POST:
            if organization.organization_picture:
                organization.organization_picture.delete()
            return redirect("exec_panel:organization-edit:index")
        organization_picture_file_name = None
        if 'organization_picture' in request.FILES and organization.organization_picture:
            organization_picture_file_name = organization.organization_picture.name

        form = OrganizationEditForm(request.POST, request.FILES, instance=organization)
        if form.is_valid():
            if organization_picture_file_name: default_storage.delete(organization_picture_file_name)
            form.save()
            return redirect("exec_panel:organization-edit:index")
    else:
        form = OrganizationEditForm(instance=organization)

    return render(request, "organization_edit/edit.html", {"active_tab": "organization-edit", "form": form, "organization": organization})
