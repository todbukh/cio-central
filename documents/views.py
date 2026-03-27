from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404

from core.permissions import is_executive
from .forms import DocumentUploadForm
from .models import Document


def index(request):


    
    # handle file uplod from the form
    if request.method == "POST":
        # only exec/owner allowed to upload
        if not is_executive(request.user):
            raise Http404()

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
        "form": DocumentUploadForm(),
        "can_upload": is_executive(request.user),
    }
    return render(request, "documents/index.html", context)



def delete_file(request, file_id):
    if request.method == "POST":
        document = get_object_or_404(Document, id=file_id)
        # remove file from storage
        document.file.delete()
        # remove it from database
        document.delete()

    return redirect("documents:index")



def view_document(request, file_id):
    document = get_object_or_404(Document, id=file_id)

    if not document.file:
        raise Http404("File not found")

   # render the file inside the site instead of redirecting to s3
    context = {
        "document": document,
        "file_url": document.file.url,
        "file_name": document.file.name.split("/")[-1],
    }
    return render(request, "documents/view_document.html", context)