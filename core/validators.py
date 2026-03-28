from django import forms

# limit 5 MB
MAX_FILE_SIZE = 5 * 1024 * 1024  

def validate_file_size(uploaded_file):
    if uploaded_file.size > MAX_FILE_SIZE:
        raise forms.ValidationError("File size must be 5 MB or smaller.")