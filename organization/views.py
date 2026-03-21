from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *


@login_required(login_url="/login/")
def home_redirect(request):
    return redirect(to="organization:messages", channel="general")


@login_required(login_url="/login/")
def messages(request, channel):
    get_object_or_404(Channel, name=channel)

    message_list = list(Message.objects.all().filter(channel__name=channel))
    message_list.sort(key=lambda message : message.sent_at)

    context = {
        "active_channel": channel,
        "channels": list(Channel.objects.all()),
        "messages": message_list
    }

    return render(request, 'organization/home.html', context)
