from rest_framework import serializers
from .models import DailyRecord, AccessRecord
from django.contrib.auth.models import User


class DailyRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DailyRecord
        fields = ["id", "user_id", "date", "go_time", "leave_time", "working_time", "break_time"]


class AccessRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccessRecord
        fields = ["id", "user_id", "tag", "check_time"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]
