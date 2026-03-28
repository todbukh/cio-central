from django import forms
from core.validators import validate_file_size

ALLOWED_FILE_TYPES = [
    "application/pdf",
    "image/png",
    "image/jpeg",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/plain",
]


class DocumentUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data.get("file")

        if file.content_type not in ALLOWED_FILE_TYPES:
            raise forms.ValidationError("File type not supported")
        
        validate_file_size(file)

        return file