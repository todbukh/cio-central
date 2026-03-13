import os

from django.conf import settings
from django.shortcuts import redirect, render
from django.http import FileResponse, Http404


def index(request):
    documents_folder = os.path.join(settings.BASE_DIR, "documents", "files")
    os.makedirs(documents_folder, exist_ok=True)
    
    # handle file uplod from the form
    if request.method == "POST":
        uploaded_file = request.FILES.get("document_file")

        if uploaded_file:
            file_path = os.path.join(documents_folder, uploaded_file.name)

            # write the file to the local doc folders
            with open(file_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

        return redirect("documents:index")
    

    files = []
    
    for name in os.listdir(documents_folder):
        file_path = os.path.join(documents_folder, name)
        # make sure we only add files and not something likefolders
        if os.path.isfile(file_path):
            files.append(name)
            

    files.sort()

    query = request.GET.get("q", "").strip()

    # filter the file list if user searched something
    if query != "":
        matching_files = []

        for file_name in files:
            if query.lower() in file_name.lower():
                matching_files.append(file_name)

        files = matching_files

    context = {
        "files": files,
        "query": query,
    }
    return render(request, "documents/index.html", context)



def delete_file(request, file_name):
    if request.method == "POST":
        documents_folder = os.path.join(settings.BASE_DIR, "documents", "files")
        file_path = os.path.join(documents_folder, file_name)

        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)

    return redirect("documents:index")



def view_document(request, filename):
    documents_folder = os.path.join(settings.BASE_DIR, "documents", "files")
    file_path = os.path.join(documents_folder, filename)

    if not os.path.exists(file_path):
        raise Http404("File not found")
    
    #return the file so the browser can open/download it
    return FileResponse(open(file_path, "rb"))