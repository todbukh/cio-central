from django.shortcuts import render

from s3_demo.forms import S3Form
from s3_demo.models import MyS3Image


def upload_image_for_user(user, image):
    if hasattr(user, "my_s3_image"):
        user.my_s3_image.image.delete()
        user.my_s3_image.image.save(name=image.name, content=image)
    else:
        user.my_s3_image = MyS3Image(user=user, image=image)
        user.my_s3_image.save()

# Create your views here.
def s3_demo(request):
    context = {
        "form": S3Form(),
        "error": False
    }

    if request.method == "POST":
        filled_form = S3Form(request.POST, request.FILES)
        if filled_form.is_valid():
            upload_image_for_user(request.user, request.FILES["image"])
        else:
            context["error"] = True

    if hasattr(request.user, "my_s3_image"):
        context["my_s3_image"] = request.user.my_s3_image.image

    return render(request, "s3_demo/s3demo.html", context=context)