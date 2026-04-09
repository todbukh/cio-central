from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse
from django.db import IntegrityError

from core.models import User
from organization.models import Channel, Message

from .models import Poll, Vote


def make_exec_user(username="exec_user"):
    return User.objects.create_user(
        username=username,
        password="testpass123",
        role=User.Role.EXEC,
        status=User.Status.APPROVED,
    )


def make_member_user(username="member_user"):
    return User.objects.create_user(
        username=username,
        password="testpass123",
        role=User.Role.MEMBER,
        status=User.Status.APPROVED,
    )


class PollFlowTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.exec_user = make_exec_user()
        self.member_user = make_member_user()

    def valid_poll_payload(self):
        return {
            "question": "Where should we hold the social?",
            "option_1": "Rice Hall",
            "option_2": "Clark Hall",
            "option_3": "Olsson Hall",
            "option_4": "",
        }

    def create_poll(self):
        self.client.force_login(self.exec_user)
        response = self.client.post(reverse("exec_panel:polls:poll_create"), self.valid_poll_payload())
        self.assertEqual(response.status_code, 302)
        return Poll.objects.get()

    def test_exec_can_create_poll_and_announcement(self):
        self.client.force_login(self.exec_user)

        response = self.client.post(reverse("exec_panel:polls:poll_create"), self.valid_poll_payload())

        poll = Poll.objects.get()
        self.assertRedirects(response, reverse("exec_panel:polls:poll_detail", args=[poll.uid]))
        self.assertEqual(poll.options.count(), 3)
        announcement = Message.objects.get(channel__name="announcements")
        self.assertIn("Poll: Where should we hold the social?", announcement.text)
        self.assertIn(reverse("polls:poll_detail", args=[poll.uid]), announcement.text)

    def test_non_exec_cannot_access_exec_create(self):
        self.client.force_login(self.member_user)
        response = self.client.get(reverse("exec_panel:polls:poll_create"))
        self.assertEqual(response.status_code, 302)

    def test_create_poll_rolls_back_if_announcement_fails(self):
        self.client.force_login(self.exec_user)

        with patch("polls.views.Message.objects.create", side_effect=IntegrityError("boom")):
            response = self.client.post(reverse("exec_panel:polls:poll_create"), self.valid_poll_payload())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "We could not publish the poll announcement")
        self.assertEqual(Poll.objects.count(), 0)
        self.assertEqual(Message.objects.count(), 0)

    def test_create_poll_re_raises_unexpected_errors(self):
        self.client.force_login(self.exec_user)

        with patch("polls.views.Message.objects.create", side_effect=RuntimeError("boom")):
            with self.assertRaises(RuntimeError):
                self.client.post(reverse("exec_panel:polls:poll_create"), self.valid_poll_payload())

    def test_create_poll_with_missing_announcements_channel_fails_cleanly(self):
        Channel.objects.filter(name="announcements").delete()
        self.client.force_login(self.exec_user)

        response = self.client.post(reverse("exec_panel:polls:poll_create"), self.valid_poll_payload())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "announcements channel is missing")
        self.assertEqual(Poll.objects.count(), 0)

    def test_member_can_vote_once(self):
        poll = self.create_poll()
        self.client.force_login(self.member_user)

        response = self.client.post(
            reverse("polls:poll_vote", args=[poll.uid]),
            {"option": str(poll.options.first().id)},
        )

        self.assertRedirects(response, reverse("polls:poll_detail", args=[poll.uid]))
        vote = Vote.objects.get(poll=poll, user=self.member_user)
        self.assertEqual(vote.option, poll.options.first())

    def test_duplicate_vote_submission_keeps_single_vote(self):
        poll = self.create_poll()
        option = poll.options.first()
        Vote.objects.create(poll=poll, option=option, user=self.member_user)
        self.client.force_login(self.member_user)

        response = self.client.post(
            reverse("polls:poll_vote", args=[poll.uid]),
            {"option": str(option.id)},
        )

        self.assertRedirects(response, reverse("polls:poll_detail", args=[poll.uid]))
        self.assertEqual(Vote.objects.filter(poll=poll, user=self.member_user).count(), 1)

    def test_duplicate_vote_integrity_error_is_handled(self):
        poll = self.create_poll()
        self.client.force_login(self.member_user)

        with patch("polls.views.Vote.objects.create", side_effect=IntegrityError("boom")):
            response = self.client.post(
                reverse("polls:poll_vote", args=[poll.uid]),
                {"option": str(poll.options.first().id)},
            )

        self.assertRedirects(response, reverse("polls:poll_detail", args=[poll.uid]))
        self.assertEqual(Vote.objects.count(), 0)

    def test_member_cannot_see_results_while_open(self):
        poll = self.create_poll()
        option = poll.options.first()
        Vote.objects.create(poll=poll, option=option, user=self.member_user)
        self.client.force_login(self.member_user)

        response = self.client.get(reverse("polls:poll_detail", args=[poll.uid]))

        self.assertNotContains(response, "<h4 class=\"mb-0\">Results</h4>", html=False)
        self.assertContains(response, "recorded")

    def test_exec_can_see_results_while_open(self):
        poll = self.create_poll()
        option = poll.options.first()
        Vote.objects.create(poll=poll, option=option, user=self.member_user)
        self.client.force_login(self.exec_user)

        response = self.client.get(reverse("polls:poll_detail", args=[poll.uid]))

        self.assertContains(response, "Results")
        self.assertContains(response, option.text)

    def test_member_sees_results_after_close(self):
        poll = self.create_poll()
        option = poll.options.first()
        Vote.objects.create(poll=poll, option=option, user=self.member_user)
        poll.close()
        self.client.force_login(self.member_user)

        response = self.client.get(reverse("polls:poll_detail", args=[poll.uid]))

        self.assertContains(response, "Results")
        self.assertContains(response, option.text)

    def test_closed_poll_rejects_vote(self):
        poll = self.create_poll()
        poll.close()
        self.client.force_login(self.member_user)

        response = self.client.post(
            reverse("polls:poll_vote", args=[poll.uid]),
            {"option": str(poll.options.first().id)},
        )

        self.assertRedirects(response, reverse("polls:poll_detail", args=[poll.uid]))
        self.assertEqual(Vote.objects.count(), 0)

    def test_unknown_poll_returns_404(self):
        import uuid

        self.client.force_login(self.member_user)
        response = self.client.get(reverse("polls:poll_detail", args=[uuid.uuid4()]))
        self.assertEqual(response.status_code, 404)

    def test_exec_can_close_poll(self):
        poll = self.create_poll()
        self.client.force_login(self.exec_user)

        response = self.client.post(reverse("exec_panel:polls:poll_close", args=[poll.uid]))

        self.assertRedirects(response, reverse("exec_panel:polls:poll_detail", args=[poll.uid]))
        poll.refresh_from_db()
        self.assertTrue(poll.is_closed)

    def test_poll_announcement_renders_button_like_ui_and_normal_messages_stay_plain(self):
        poll = self.create_poll()
        Message.objects.create(
            channel=Channel.objects.get(name="announcements"),
            user=self.exec_user,
            text="Regular update for everyone.",
        )
        self.client.force_login(self.member_user)

        response = self.client.get(reverse("organization:messages", args=["announcements"]))

        self.assertContains(response, "Open Poll")
        self.assertContains(response, reverse("polls:poll_detail", args=[poll.uid]))
        self.assertContains(response, "Regular update for everyone.")
