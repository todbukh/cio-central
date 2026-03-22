from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from core.models import User
from .models import Event


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


def make_event(**kwargs):
    defaults = {
        "name": "Test Event",
        "date": timezone.now(),
        "description": "A test event description.",
    }
    defaults.update(kwargs)
    return Event.objects.create(**defaults)


class EventModelTest(TestCase):

    def test_str_returns_name(self):
        event = make_event(name="Annual Gala")
        self.assertEqual(str(event), "Annual Gala")

    def test_uid_auto_generated(self):
        event = make_event()
        self.assertIsNotNone(event.uid)

    def test_events_ordered_by_date(self):
        later = make_event(name="Later", date=timezone.now() + timezone.timedelta(days=5))
        sooner = make_event(name="Sooner", date=timezone.now() + timezone.timedelta(days=1))
        events = list(Event.objects.all())
        self.assertEqual(events[0], sooner)
        self.assertEqual(events[1], later)

    def test_description_optional(self):
        event = make_event(description="")
        self.assertEqual(event.description, "")


class EventFormTest(TestCase):

    def test_valid_form(self):
        from .forms import EventForm
        form = EventForm(data={
            "name": "My Event",
            "date": "2030-06-15T10:00",
            "description": "Some details.",
        })
        self.assertTrue(form.is_valid())

    def test_missing_name_invalid(self):
        from .forms import EventForm
        form = EventForm(data={
            "name": "",
            "date": "2030-06-15T10:00",
            "description": "Some details.",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_missing_date_invalid(self):
        from .forms import EventForm
        form = EventForm(data={
            "name": "My Event",
            "date": "",
            "description": "Some details.",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("date", form.errors)

    def test_description_not_required(self):
        from .forms import EventForm
        form = EventForm(data={
            "name": "My Event",
            "date": "2030-06-15T10:00",
            "description": "",
        })
        self.assertTrue(form.is_valid())

    def test_description_max_length(self):
        from .forms import EventForm
        form = EventForm(data={
            "name": "My Event",
            "date": "2030-06-15T10:00",
            "description": "x" * 2001,
        })
        self.assertFalse(form.is_valid())
        self.assertIn("description", form.errors)


class EventViewPermissionTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.exec_user = make_exec_user()
        self.member_user = make_member_user()
        self.event = make_event()

    def test_events_list_requires_exec(self):
        self.client.force_login(self.member_user)
        response = self.client.get(reverse("exec_panel:events:events"))
        self.assertNotEqual(response.status_code, 200)

    def test_events_list_accessible_to_exec(self):
        self.client.force_login(self.exec_user)
        response = self.client.get(reverse("exec_panel:events:events"))
        self.assertEqual(response.status_code, 200)

    def test_event_detail_accessible_to_exec(self):
        self.client.force_login(self.exec_user)
        response = self.client.get(reverse("exec_panel:events:event_detail", args=[self.event.uid]))
        self.assertEqual(response.status_code, 200)

    def test_event_create_accessible_to_exec(self):
        self.client.force_login(self.exec_user)
        response = self.client.get(reverse("exec_panel:events:event_create"))
        self.assertEqual(response.status_code, 200)


class EventCRUDTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.exec_user = make_exec_user()
        self.client.force_login(self.exec_user)

    def test_create_event(self):
        response = self.client.post(reverse("exec_panel:events:event_create"), {
            "name": "New Event",
            "date": "2030-08-01T09:00",
            "description": "Details here.",
        })
        self.assertRedirects(response, reverse("exec_panel:events:events"))
        self.assertTrue(Event.objects.filter(name="New Event").exists())

    def test_edit_event(self):
        event = make_event(name="Old Name")
        response = self.client.post(
            reverse("exec_panel:events:event_edit", args=[event.uid]),
            {"name": "New Name", "date": "2030-08-01T09:00", "description": ""},
        )
        self.assertRedirects(response, reverse("exec_panel:events:events"))
        event.refresh_from_db()
        self.assertEqual(event.name, "New Name")

    def test_delete_event_post(self):
        event = make_event()
        response = self.client.post(reverse("exec_panel:events:event_delete", args=[event.uid]))
        self.assertRedirects(response, reverse("exec_panel:events:events"))
        self.assertFalse(Event.objects.filter(uid=event.uid).exists())

    def test_delete_event_get_does_not_delete(self):
        event = make_event()
        self.client.get(reverse("exec_panel:events:event_delete", args=[event.uid]))
        self.assertTrue(Event.objects.filter(uid=event.uid).exists())

    def test_detail_returns_404_for_unknown_uid(self):
        import uuid
        fake_uid = uuid.uuid4()
        response = self.client.get(reverse("exec_panel:events:event_detail", args=[fake_uid]))
        self.assertEqual(response.status_code, 404)
