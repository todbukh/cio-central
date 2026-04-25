from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
import re

from core.decorators import executive_required
from events.models import Event
from organization_edit.models import Organization
from .forms import MessageForm, ChannelForm
from .models import Channel, Message


POLL_ANNOUNCEMENT_PATTERN = re.compile(
    r"^Poll: (?P<question>.+)\nVote here: (?P<url>/polls/[0-9a-f-]+/)$"
)

EVENT_ANNOUNCEMENT_PATTERN = re.compile(
    r"^Event: (?P<name>.+)\nView details: (?P<url>/events/[0-9a-f-]+/)$"
)


def enrich_poll_announcements(messages):
    for message in messages:
        match = POLL_ANNOUNCEMENT_PATTERN.match(message.text)
        message.poll_url = None
        message.poll_question = None

        if match:
            message.poll_url = match.group("url")
            message.poll_question = match.group("question")

    return messages


def enrich_event_announcements(messages):
    for message in messages:
        match = EVENT_ANNOUNCEMENT_PATTERN.match(message.text)
        message.event_url = None
        message.event_name = None
        message.exec_event_url = None

        if match:
            message.event_name = match.group("name")
            uid = match.group("url").strip("/").split("/")[-1]
            if Event.objects.filter(uid=uid).exists():
                message.event_url = match.group("url")
                message.exec_event_url = reverse("exec_panel:events:event_detail", args=[uid])

    return messages


@login_required(login_url="/login/")
def home_redirect(request):
    return redirect(to="organization:messages", channel="general")


@login_required(login_url="/login/")
def messages(request, channel):
    active_channel = get_object_or_404(Channel, name=channel)

    organization, created = Organization.objects.get_or_create(
        id=0
    )

    if request.method == "POST":
        # redirect if user does not have permission to post in channel
        if active_channel.exec_only and not request.user.is_exec():
            return redirect("organization:messages", channel=channel)

        form = MessageForm(request.POST)
        if form.is_valid():
            message = Message(channel=active_channel, user=request.user, text=form.cleaned_data["text"])
            message.save()
            return redirect("organization:messages", channel=channel)

    # copilot suggested use of select_related to solve N+1 problem
    message_list = list(
        Message.objects
            .filter(channel__name=channel)
            .select_related("user__profile")
            .order_by("sent_at")
    )
    enrich_poll_announcements(message_list)
    enrich_event_announcements(message_list)

    today = timezone.localdate()
    today_events = list(Event.objects.filter(date__date=today))

    org_img_url = None
    if organization.organization_picture: org_img_url = organization.organization_picture.url

    context = {
        "active_channel": active_channel,
        "channels": list(Channel.objects.all()),
        "messages": message_list,
        "today_events": today_events,
        "org_name": organization.name,
        "org_img_url": org_img_url,
    }

    return render(request, 'organization/home.html', context)


@require_POST
@login_required(login_url="/login/")
def delete_message(request):
    # credit to Claude Opus 4.6 for suggesting get_object_or_404 and .get("id")
    message_id = request.POST.get("id")
    if message_id is None: raise Http404("Message does not exist")
    message = get_object_or_404(Message, id=message_id)

    channel_name = message.channel.name

    if request.user.is_exec() or request.user.username == message.user.username:
        message.delete()
    else:  # credit to Claude Opus 4.6 for suggesting returning the forbidden code instead of just a redirect
        return HttpResponseForbidden()

    return redirect("organization:messages", channel=channel_name)


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
