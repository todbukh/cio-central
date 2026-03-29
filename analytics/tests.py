from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from attendance.models import Attendance
from events.models import Event


settings.SECRET_KEY = "test-secret-key"


class AnalyticsViewTests(TestCase):
    def setUp(self):
        self.url = reverse("exec_panel:analytics:analytics")
        user_model = get_user_model()
        self.exec_user = user_model.objects.create_user(
            username="exec-user",
            password="password123",
            first_name="Exec",
            last_name="User",
            role=user_model.Role.EXEC,
            status=user_model.Status.APPROVED,
        )
        self.member_user = user_model.objects.create_user(
            username="member-user",
            password="password123",
            first_name="Member",
            last_name="User",
            role=user_model.Role.MEMBER,
            status=user_model.Status.APPROVED,
        )
        self.other_member = user_model.objects.create_user(
            username="other-member",
            password="password123",
            first_name="Other",
            last_name="Member",
            role=user_model.Role.MEMBER,
            status=user_model.Status.APPROVED,
        )

        now = timezone.now()
        self.past_event = Event.objects.create(
            name="Spring Kickoff",
            date=now - timedelta(days=2),
            created_by=self.exec_user,
        )
        self.older_past_event = Event.objects.create(
            name="Hack Night",
            date=now - timedelta(days=5),
            created_by=self.exec_user,
        )
        self.future_event = Event.objects.create(
            name="Future Planning",
            date=now + timedelta(days=2),
            created_by=self.exec_user,
        )

        Attendance.objects.create(
            member=self.exec_user,
            event=self.past_event,
            status=Attendance.Status.PRESENT,
        )
        Attendance.objects.create(
            member=self.member_user,
            event=self.past_event,
            status=Attendance.Status.ABSENT,
        )
        Attendance.objects.create(
            member=self.other_member,
            event=self.past_event,
            status=Attendance.Status.PRESENT,
        )
        Attendance.objects.create(
            member=self.exec_user,
            event=self.older_past_event,
            status=Attendance.Status.PRESENT,
        )
        Attendance.objects.create(
            member=self.member_user,
            event=self.older_past_event,
            status=Attendance.Status.PRESENT,
        )

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, f"/login/?next={self.url}")

    def test_non_exec_user_is_redirected_home(self):
        self.client.force_login(self.member_user)

        response = self.client.get(self.url)

        self.assertRedirects(response, reverse("organization:home"), fetch_redirect_response=False)

    def test_exec_user_sees_real_user_analytics_by_default(self):
        self.client.force_login(self.exec_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_view"], "users")
        self.assertContains(response, "Exec User")
        self.assertContains(response, "Other Member")
        self.assertContains(response, "100%")
        self.assertContains(response, "50%")
        self.assertContains(response, "Tracked members")
        self.assertContains(response, reverse("exec_panel:analytics:user_detail", args=[self.exec_user.uid]))
        self.assertEqual(response.context["summary_cards"][0]["value"], 3)
        self.assertEqual(response.context["summary_cards"][1]["value"], 2)
        self.assertEqual(response.context["summary_cards"][2]["value"], 2)

    def test_exec_user_can_switch_to_real_event_analytics(self):
        self.client.force_login(self.exec_user)

        response = self.client.get(self.url, {"view": "events"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_view"], "events")
        self.assertEqual(response.context["chart_title"], "Recent event turnout overview")
        self.assertContains(response, "Showing the 3 most recent past events")
        self.assertContains(response, "Spring Kickoff")
        self.assertContains(response, "Hack Night")
        self.assertContains(response, reverse("exec_panel:attendance:event_attendance", args=[self.past_event.uid]))
        self.assertContains(response, "67%")
        self.assertContains(response, "100%")

    def test_future_events_are_excluded_from_analytics(self):
        self.client.force_login(self.exec_user)

        response = self.client.get(self.url, {"view": "events"})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Future Planning")

    def test_invalid_view_falls_back_to_user_analytics(self):
        self.client.force_login(self.exec_user)

        response = self.client.get(self.url, {"view": "bad"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_view"], "users")
        self.assertContains(response, "Per-user analytics")
        self.assertContains(response, "Exec User")

    def test_exec_user_can_view_user_detail_page(self):
        self.client.force_login(self.exec_user)

        response = self.client.get(reverse("exec_panel:analytics:user_detail", args=[self.member_user.uid]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Member User")
        self.assertContains(response, "Hack Night")
        self.assertContains(response, "Spring Kickoff")
        self.assertContains(response, "PRESENT")
        self.assertContains(response, "ABSENT")

    def test_non_exec_user_cannot_view_user_detail_page(self):
        self.client.force_login(self.member_user)

        response = self.client.get(reverse("exec_panel:analytics:user_detail", args=[self.exec_user.uid]))

        self.assertRedirects(response, reverse("organization:home"), fetch_redirect_response=False)
