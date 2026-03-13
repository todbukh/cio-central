import os

from django.conf import settings
from django.shortcuts import redirect, render


def index(request):
    documents_folder = os.path.join(settings.BASE_DIR, "documents", "files")
    os.makedirs(documents_folder, exist_ok=True)

    if request.method == "POST":
        uploaded_file = request.FILES.get("document_file")

        if uploaded_file:
            file_path = os.path.join(documents_folder, uploaded_file.name)

            with open(file_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

        return redirect("documents:index")
    

    files = []

    for name in os.listdir(documents_folder):
        file_path = os.path.join(documents_folder, name)
        if os.path.isfile(file_path):
            files.append(name)
            

    files.sort()

    query = request.GET.get("q", "").strip()

    if query:
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