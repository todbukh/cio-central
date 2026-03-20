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
        ],
        "messages": [
            {
                "username": "kenningspath",
                "timestamp": "3/20/26, 10:05AM",
                "text": "Hey, did you see the update on the repo? I finally merged that PR for the landing page layout but the CSS is still acting a bit weird on mobile. It looks fine on Chrome but Safari is doing that weird overlapping thing again."
            },
            {
                "username": "todbukh",
                "timestamp": "3/20/26, 10:12AM",
                "text": "Safari is literally the new IE. I haven't checked it yet but I'll pull the changes after I finish this coffee. My morning has been a total wash because my keyboard decided to stop responding and I had to dig out an old membrane one from the closet."
            },
            {
                "username": "kenningspath",
                "timestamp": "3/20/26, 10:15AM",
                "text": "Ugh, membrane keys are the worst. It’s like typing on wet sponges. Anyway, no rush on the code, I’m probably going to take a break and go for a walk anyway because I’ve been staring at this flexbox issue for two hours and I’m starting to lose my mind."
            },
            {
                "username": "todbukh",
                "timestamp": "3/20/26, 10:22AM",
                "text": "Fair. Hey, did you ever find that specific screwdriver set you were looking for? The one with the precision bits for the laptop case? I think I might have left mine at your place last time we were working on the server rack or I might have just lost it in my car."
            },
            {
                "username": "kenningspath",
                "timestamp": "3/20/26, 10:35AM",
                "text": "I actually found it! It was tucked behind the monitor stand. I’ll bring it over next time we meet up. Also, I just checked the logs and it looks like the database migration went through without any errors, which is a huge relief considering how much of a mess the schema was."
            },
            {
                "username": "todbukh",
                "timestamp": "3/20/26, 10:48AM",
                "text": "That’s actually huge news. I was genuinely worried we were going to lose the metadata for the older entries. I’m going to start working on the API documentation now so we can actually show the rest of the team how to query the new endpoints without them having to ask us every five minutes."
            },
            {
                "username": "kenningspath",
                "timestamp": "3/20/26, 11:02AM",
                "text": "Lol good luck with that. You know they’re still going to ask anyway. By the way, are we still on for that Thai place for lunch or are you too swamped with the docs? I’m starving and I really don’t want to eat another sad desk salad today."
            },
            {
                "username": "todbukh",
                "timestamp": "3/20/26, 11:05AM",
                "text": "Definitely still on. I need to get out of this house. My neighbor has been running a power saw since 8 AM and I can't concentrate on anything. Give me like twenty minutes to wrap up this one section and then I’ll head over to your place."
            },
            {
                "username": "kenningspath",
                "timestamp": "3/20/26, 11:10AM",
                "text": "Sounds good. I'll be ready. I just realized I left my car at the shop for an oil change so we'll have to take yours if that's okay. They said it would be ready by 3 PM but they always take longer than they say they will, especially on a Friday."
            },
            {
                "username": "todbukh",
                "timestamp": "3/20/26, 11:12AM",
                "text": "No worries, I'll swing by and pick you up. See you in a bit."
            }
        ]
    }

    return render(request, 'organization/home.html', context)
