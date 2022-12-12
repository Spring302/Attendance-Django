from django.test import TestCase
from django.utils import timezone

from .validators import is_tag_in_or_out
from .utils.utils import *
from .views import AccessRecordList
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from django.contrib.auth import get_user_model


class AccessRecordTests(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_superuser("template", "admin@myproject.com", "template")

    def test_access_with_future_record(self):
        future_time = {"check_time": str(timezone.now() + timedelta(days=1))}
        self.assertTrue(is_record_future_time(future_time))

    def test_access_with_recent_record(self):
        recent_time = {"check_time": str(timezone.now())}
        self.assertFalse(is_record_future_time(recent_time))

    def test_access_with_old_record(self):
        old_time = {"check_time": str(timezone.now() - timedelta(days=1))}
        self.assertFalse(is_record_future_time(old_time))

    def test_tag_is_not_in_or_out(self):
        self.assertTrue(is_tag_in_or_out("ININ"))

    def test_post_list(self):
        # Using the standard RequestFactory API to create a form POST request
        factory = APIRequestFactory()
        request = factory.post("/access/", {"user_id": 1, "tag": "IN"})
        view = AccessRecordList.as_view()
        User = get_user_model()
        user = User.objects.get(username="template")
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
