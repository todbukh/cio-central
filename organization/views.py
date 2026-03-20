from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
@login_required(login_url="/login/")
def home(request, channel):
    context = {
        "active_channel": channel,
        "channels": [
            "general", "announcements"
        ]
    }

    return render(request, 'organization/home.html', context)
