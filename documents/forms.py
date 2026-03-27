from django import forms

ALLOWED_FILE_TYPES = [
    "application/pdf",
    "image/png",
    "image/jpeg",
]


class DocumentUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data.get("file")

        if file.content_type not in ALLOWED_FILE_TYPES:
            raise forms.ValidationError("File type not supported")

        return file