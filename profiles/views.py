from django.shortcuts import render


def profile_view(request):
    context = {
        "username": "John Smith",       # placeholder — real data comes later
        "bio": "This is my bio.",     # placeholder
    }
    return render(request, "profiles/profile.html", context)
