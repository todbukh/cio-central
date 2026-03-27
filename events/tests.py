from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from core.models import User
from .forms import EventForm
from .models import Event

# helper functions to create test data for unit testing

# make an executive user
def make_exec_user(username="exec_user"):
    return User.objects.create_user(
        username=username,
        password="testpass123",
        role=User.Role.EXEC,
        status=User.Status.APPROVED,
    )

# make a member user
def make_member_user(username="member_user"):
    return User.objects.create_user(
        username=username,
        password="testpass123",
        role=User.Role.MEMBER,
        status=User.Status.APPROVED,
    )

# make an event with default values that can be overridden by kwargs
def make_event(**kwargs):
    defaults = {
        "name": "Test Event",
        "date": timezone.now(),
        "description": "A test event description.",
    }
    defaults.update(kwargs)
    return Event.objects.create(**defaults)

# Test cases for the Event model, form, and views
class EventModelTest(TestCase):
     # Test that the string representation of an event is its name (not that important)
    def test_str_returns_name(self):
        event = make_event(name="Annual Gala")
        self.assertEqual(str(event), "Annual Gala")

    # Test that the uid field is automatically generated in event model upon creation
    def test_uid_auto_generated(self):
        event = make_event()
        self.assertIsNotNone(event.uid)

    # Test that events are ordered by date in ascending order (soonest first)
    def test_events_ordered_by_date(self):
        later = make_event(name="Later", date=timezone.now() + timezone.timedelta(days=5))
        sooner = make_event(name="Sooner", date=timezone.now() + timezone.timedelta(days=1))
        events = list(Event.objects.all())
        self.assertEqual(events[0], sooner)
        self.assertEqual(events[1], later)

    # Test that description is optional and can be blank
    def test_description_optional(self):
        event = make_event(description="")
        self.assertEqual(event.description, "")

    # Test that description is optional and can be blank
    def test_location_optional(self):
        event = make_event(location="")
        self.assertEqual(event.location, "")

    # Test that location is stored correctly when provided
    def test_location_stored(self):
        event = make_event(location="Rice Hall")
        self.assertEqual(event.location, "Rice Hall")

# Test cases for the EventForm
class EventFormTest(TestCase):

    # Test that a valid form with all fields filled in is valid
    def test_valid_form(self):
        form = EventForm(data={
            "name": "My Event",
            "date": "2030-06-15T10:00",
            "description": "Some Valid Description!",
        })
        self.assertTrue(form.is_valid())

    # Test that an event without a name is invalid, since name is required
    def test_missing_name_invalid(self):
        form = EventForm(data={
            "name": "",
            "date": "2030-06-15T10:00",
            "description": "Some Valid Description!",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    # Test that an event without a date is invalid, since date is required
    def test_missing_date_invalid(self):
        form = EventForm(data={
            "name": "My Event",
            "date": "",
            "description": "Some Valid Description!",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("date", form.errors)

    # test that eveent without description is still valid, since description is optional
    def test_description_not_required(self):
        form = EventForm(data={
            "name": "My Event",
            "date": "2030-06-15T10:00",
            "description": "",
        })
        self.assertTrue(form.is_valid())

    # Test that an event with a description longer than 2000 characters is invalid
    def test_description_max_length(self):
        form = EventForm(data={
            "name": "My Event",
            "date": "2030-06-15T10:00",
            "description": "x" * 2001,
        })
        self.assertFalse(form.is_valid())
        self.assertIn("description", form.errors)

    # Test that an event without a location is still valid, since location is optional
    def test_location_not_required(self):
        form = EventForm(data={
            "name": "My Event",
            "date": "2030-06-15T10:00",
            "location": "",
            "description": "",
        })
        self.assertTrue(form.is_valid())

    # Test that an event with a location longer than 100 characters is invalid
    def test_location_max_length(self):
        form = EventForm(data={
            "name": "My Event",
            "date": "2030-06-15T10:00",
            "location": "x" * 101,
            "description": "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("location", form.errors)

    # Test that an event with a location is valid and stored correctly
    def test_valid_form_with_location(self):
        form = EventForm(data={
            "name": "My Event",
            "date": "2030-06-15T10:00",
            "location": "Rice Hall",
            "description": "Some details.",
        })
        self.assertTrue(form.is_valid())

# Test cases for the Event views, using the test client to simulate requests
class EventViewPermissionTest(TestCase):
    # Client() --> create a fake web browser that we can use to simulate requests to our views and test the responses. 
    # create one exec user and one member user to test permissions of views
    # create one event for detail-page tests
    def setUp(self):
        self.client = Client()
        self.exec_user = make_exec_user()
        self.member_user = make_member_user()
        self.event = make_event()

    # 200 is an HTTP status code that means:
    # The request succeeded and the server returned the page

    # a normal member should not be able to access the events management list
    def test_events_list_requires_exec(self):
        self.client.force_login(self.member_user)
        response = self.client.get(reverse("exec_panel:events:events"))
        self.assertNotEqual(response.status_code, 200)

    # an exec user should be able to access the page
    def test_events_list_accessible_to_exec(self):
        self.client.force_login(self.exec_user)
        response = self.client.get(reverse("exec_panel:events:events"))
        self.assertEqual(response.status_code, 200)

    # Checks that the exec user can access the event detail page.
    def test_event_detail_accessible_to_exec(self):
        self.client.force_login(self.exec_user)
        response = self.client.get(reverse("exec_panel:events:event_detail", args=[self.event.uid]))
        self.assertEqual(response.status_code, 200)

    # Checks that the exec user can access the event creation page.
    def test_event_create_accessible_to_exec(self):
        self.client.force_login(self.exec_user)
        response = self.client.get(reverse("exec_panel:events:event_create"))
        self.assertEqual(response.status_code, 200)

# Test cases for creating, editing, and deleting events through the views
class EventCRUDTest(TestCase):

    # This means every test in this class starts with:
    # a fresh client
    # a valid authorized user already logged in
    def setUp(self):
        self.client = Client()
        self.exec_user = make_exec_user()
        self.client.force_login(self.exec_user)

    # checks:
    # POST to create view works
    # successful create redirects properly
    # event was actually inserted into DB
    def test_create_event(self):
        response = self.client.post(reverse("exec_panel:events:event_create"), {
            "name": "New Event",
            "date": "2030-08-01T09:00",
            "description": "Details here.",
        })
        self.assertRedirects(response, reverse("exec_panel:events:events"))
        self.assertTrue(Event.objects.filter(name="New Event").exists())

    # checks that an optional field like location is actually saved correctly
    def test_create_event_with_location(self):
        response = self.client.post(reverse("exec_panel:events:event_create"), {
            "name": "Located Event",
            "date": "2030-08-01T09:00",
            "location": "Rice Hall",
            "description": "",
        })
        self.assertRedirects(response, reverse("exec_panel:events:events"))
        event = Event.objects.get(name="Located Event")
        self.assertEqual(event.location, "Rice Hall")

    # edit view accepts POST
    # redirect is correct
    # DB object was really updated
    def test_edit_event(self):
        event = make_event(name="Old Name")
        response = self.client.post(
            reverse("exec_panel:events:event_edit", args=[event.uid]),
            {"name": "New Name", "date": "2030-08-01T09:00", "description": ""},
        )
        self.assertRedirects(response, reverse("exec_panel:events:events"))
        event.refresh_from_db()
        self.assertEqual(event.name, "New Name")


    def test_edit_event_location(self):
        event = make_event(name="My Event", location="Old Location")
        response = self.client.post(
            reverse("exec_panel:events:event_edit", args=[event.uid]),
            {"name": "My Event", "date": "2030-08-01T09:00", "location": "New Location", "description": ""},
        )
        self.assertRedirects(response, reverse("exec_panel:events:events"))
        event.refresh_from_db()
        self.assertEqual(event.location, "New Location")

    # checks the intended delete path
    # deletion happens on POST
    # user is redirected
    # object is really gone
    def test_delete_event_post(self):
        event = make_event()
        response = self.client.post(reverse("exec_panel:events:event_delete_confirm", args=[event.uid]))
        self.assertRedirects(response, reverse("exec_panel:events:events"))
        self.assertFalse(Event.objects.filter(uid=event.uid).exists())

    # checks that visiting the delete page should not delete the object
    # GET = show page / safe
    # POST = actually delete
    def test_delete_event_get_does_not_delete(self):
        event = make_event()
        self.client.get(reverse("exec_panel:events:event_delete", args=[event.uid]))
        self.assertTrue(Event.objects.filter(uid=event.uid).exists())

    # checks error handling for invalid input
    # confirms view does not: 
    # crash, return 500 (HTTP 500 = Internal Server Error), accidentally show the wrong object, silently succeed on a bad uid
    def test_detail_returns_404_for_unknown_uid(self):
        import uuid
        fake_uid = uuid.uuid4()
        response = self.client.get(reverse("exec_panel:events:event_detail", args=[fake_uid]))
        self.assertEqual(response.status_code, 404)
