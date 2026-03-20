from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required(login_url="/login/")
def home_redirect(request):
    return redirect(to="organization:messages", channel="general")


@login_required(login_url="/login/")
def messages(request, channel):
    context = {
        "active_channel": channel,
        "channels": [
            "general", "announcements"  # TODO: fetch from channel table
        ]
    }

    return render(request, 'organization/home.html', context)
