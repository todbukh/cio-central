from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from core.decorators import executive_required
from .forms import MessageForm, ChannelForm
from .models import Channel, Message


@login_required(login_url="/login/")
def home_redirect(request):
    return redirect(to="organization:messages", channel="general")


@login_required(login_url="/login/")
def messages(request, channel):
    active_channel = get_object_or_404(Channel, name=channel)

    if request.method == "POST":
        # redirect if user does not have permission to post in channel
        if active_channel.exec_only and not request.user.is_exec():
            return redirect("organization:messages", channel=channel)

        form = MessageForm(request.POST)
        if form.is_valid():
            message = Message(channel=active_channel, user=request.user, text=form.cleaned_data["text"])
            message.save()
            return redirect("organization:messages", channel=channel)

    message_list = list(Message.objects.filter(channel__name=channel).order_by("sent_at"))

    context = {
        "active_channel": active_channel,
        "channels": list(Channel.objects.all()),
        "messages": message_list,
    }

    return render(request, 'organization/home.html', context)


@require_POST
@login_required(login_url="/login/")
def delete_message(request):
    # credit to Claude Opus 4.6 for suggesting get_object_or_404 and .get("id")
    message_id = request.POST.get("id")
    if message_id is None: raise Http404("Message does not exist")
    message = get_object_or_404(Message, id=message_id)

    if request.user.is_exec() or request.user.username == message.user.username:
        message.delete()
    else:  # credit to Claude Opus 4.6 for suggesting returning the forbidden code instead of just a redirect
        return HttpResponseForbidden()

    return redirect("organization:messages", channel=message.channel.name)


@login_required(login_url="/login/")
@executive_required(redirect_url="organization:home")
def create_channel(request):
    context = {
        "form": ChannelForm()
    }

    if request.method == "POST":
        form = ChannelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("organization:home")
        else:
            context["form"] = form

    return render(request,"organization/create_channel.html", context)


@login_required(login_url="/login/")
@executive_required(redirect_url="organization:home")
def edit_channel(request, channel):
    channel_model = get_object_or_404(Channel, name=channel)

    if channel_model.builtin: return HttpResponseForbidden()

    context = {
        "channel": channel_model,
        "form": ChannelForm(instance=channel_model)
    }

    if request.method == "POST":
        form = ChannelForm(request.POST, instance=channel_model)
        if form.is_valid():
            form.save()
            return redirect("organization:home")
        else:
            context["form"] = form

    return render(request,"organization/edit_channel.html", context)


@require_POST
@login_required(login_url="/login/")
@executive_required(redirect_url="organization:home")
def delete_channel(request, channel):
    # credit to Claude Opus 4.6 for suggesting get_object_or_404 and .get("id")
    channel_model = get_object_or_404(Channel, name=channel)

    if channel_model.builtin: return HttpResponseForbidden()

    if request.user.is_exec():
        channel_model.delete()
    else:  # credit to Claude Opus 4.6 for suggesting returning the forbidden code instead of just a redirect
        return HttpResponseForbidden()

    return redirect("organization:home")
