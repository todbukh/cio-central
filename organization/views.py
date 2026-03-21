from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import MessageForm
from .models import *


@login_required(login_url="/login/")
def home_redirect(request):
    return redirect(to="organization:messages", channel="general")


@login_required(login_url="/login/")
def messages(request, channel):
    active_channel_model = get_object_or_404(Channel, name=channel)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = Message(channel=active_channel_model, user=request.user, text=form.cleaned_data["text"])
            message.save()
            return redirect("organization:messages", channel=channel)
        else:
            message_send_error = "Messages must be 2000 characters or less"
            form_text = form["text"].data

    message_list = list(Message.objects.all().filter(channel__name=channel))
    message_list.sort(key=lambda message : message.sent_at)

    context = {
        "active_channel": channel,
        "channels": list(Channel.objects.all()),
        "messages": message_list,
    }

    return render(request, 'organization/home.html', context)
