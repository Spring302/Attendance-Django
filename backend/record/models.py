from django.db import models
from django.utils import timezone
from .utils.time_utils import *


class DailyRecord(models.Model):
    user_id = models.IntegerField(null=False)
    date = models.DateField(default=working_timezone)
    go_time = models.DateTimeField(default=timezone.now)
    leave_time = models.DateTimeField(null=True)
    working_time = models.IntegerField(default=0)
    break_time = models.IntegerField(default=0)


class AccessRecord(models.Model):
    user_id = models.IntegerField(null=False)
    tag = models.CharField(max_length=10, default="IN")
    check_time = models.DateTimeField(default=timezone.now)
