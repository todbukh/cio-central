from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404

from core.permissions import is_executive
from .forms import DocumentUploadForm
from .models import Document
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from core.decorators import executive_required
from django.core.exceptions import PermissionDenied



@login_required(login_url="/login/")
def index(request):

    # handle file uplod from the form
    if request.method == "POST":
        # only exec/owner allowed to upload
        if not is_executive(request.user):
            raise PermissionDenied

        form = DocumentUploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = form.cleaned_data["file"]
            #save the file using Django storage
            Document.objects.create(file=uploaded_file)
            return redirect("documents:index")
    

    files = list(Document.objects.all())
    # sort by the file name
    files.sort(key=lambda document: document.file.name.lower())

    query = request.GET.get("q", "").strip()

    # filter the file list if user searched something
    if query != "":
        matching_files = []

        for document in files:
            file_name = document.file.name.split("/")[-1]

            if query.lower() in file_name.lower():
                matching_files.append(document)

        files = matching_files

    context = {
        "files": files,
        "query": query,
        "form": form if request.method == "POST" else DocumentUploadForm(),
        "can_upload": is_executive(request.user),
    }
    return render(request, "documents/index.html", context)



@login_required(login_url="/login/")
@executive_required(redirect_url="documents:index")
def delete_file(request, file_uid):
    
    document = get_object_or_404(Document, uid=file_uid)

    context = {
        "document": document,
        "file_name": document.file.name.split("/")[-1],
    }
    return render(request, "documents/delete_document.html", context)


@login_required(login_url="/login/")
@require_POST
@executive_required(redirect_url="documents:index")
def delete_file_post(request, file_uid):
    
    document = get_object_or_404(Document, uid=file_uid)
    # remove file from storage
    document.file.delete(save=False)
    # remove it from database
    document.delete()
    return redirect("documents:index")



@login_required(login_url="/login/")
def view_document(request, file_uid):
    document = get_object_or_404(Document, uid=file_uid)

    if not document.file:
        raise Http404("File not found")

   
    file_name = document.file.name.split("/")[-1]
    file_url = document.file.url
    lower_file_name = file_name.lower()

    image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".webp"]
    # render the file inside the site instead of redirecting to s3
    # and render images differently so they fit better on the page
    context = {
        "document": document,
        "file_url": file_url,
        "file_name": file_name,
        "is_image": any(lower_file_name.endswith(ext) for ext in image_extensions),
    }
    return render(request, "documents/view_document.html", context)

