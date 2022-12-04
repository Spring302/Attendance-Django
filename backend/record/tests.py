from django.test import TestCase
from django.utils import timezone

from .utils.utils import *


class AccessRecordTests(TestCase):
    def test_access_record_with_future_record(self):
        future_time = {"check_time": str(timezone.now() + timedelta(days=1))}
        self.assertIs(is_record_future_time(future_time), True)

    def test_access_record_with_recent_record(self):
        recent_time = {"check_time": str(timezone.now())}
        self.assertIs(is_record_future_time(recent_time), False)

    def test_access_record_with_old_record(self):
        old_time = {"check_time": str(timezone.now() - timedelta(days=1))}
        self.assertIs(is_record_future_time(old_time), False)
