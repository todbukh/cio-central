from django.shortcuts import render, redirect

from s3_demo.forms import S3Form
from s3_demo.models import MyS3Image


# this function demonstrates how to upload an image
# images passed-in are of type UploadedFile
def upload_image_for_user(user, image):
    if hasattr(user, "my_s3_image"):
        user.my_s3_image.image.delete()
        user.my_s3_image.image.save(name=image.name, content=image)
    else:
        user.my_s3_image = MyS3Image(user=user, image=image)
        user.my_s3_image.save()


def s3_demo(request):
    context = {
        "form": S3Form(),
        "error": False,
    }

    if request.method == "POST":
        form = S3Form(request.POST, request.FILES)
        if form.is_valid():
            upload_image_for_user(request.user, request.FILES["image"])
            return redirect("s3_demo:s3_demo")  # refactored this to redirect from copilot's suggestion to avoid form resubmission
        else:
            # passing the form with an error back into the template is best practices
            # as it lets you get the error info off of it (I took this change from Copilot as well)
            context["form"] = form
            context["error"] = True

    if hasattr(request.user, "my_s3_image"):
        context["my_s3_image"] = request.user.my_s3_image.image

    return render(request, "s3_demo/s3demo.html", context=context)


def s3_demo_delete(request):
    if request.method == "GET": redirect("s3_demo:s3_demo")

    if hasattr(request.user, "my_s3_image"): request.user.my_s3_image.image.delete()

    return redirect("s3_demo:s3_demo")