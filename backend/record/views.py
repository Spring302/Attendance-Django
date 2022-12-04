from .models import DailyRecord, AccessRecord
from .serializers import DailyRecordSerializer, AccessRecordSerializer
from rest_framework import generics
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils.utils import record_daily, update_daily_now, is_record_future_time
from rest_framework import status
from rest_framework import permissions


class DailyRecordList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = DailyRecord.objects.all()
    serializer_class = DailyRecordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        update_daily_now(response.data)
        return response

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DailyRecordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DailyRecord.objects.all()
    serializer_class = DailyRecordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DailyRecordUserList(APIView):
    def get(self, request, *args, **kwargs):
        daily_record = DailyRecord.objects.filter(user_id=kwargs["user_id"])
        serializer = DailyRecordSerializer(daily_record, many=True)
        update_daily_now(serializer.data)
        return Response(serializer.data)


class AccessRecordList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = AccessRecord.objects.all()
    serializer_class = AccessRecordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if is_record_future_time(request.data):
            return Response({"error": "You cannot record future time."}, status=status.HTTP_400_BAD_REQUEST)
        response = self.create(request, *args, **kwargs)
        record_daily(request.data)
        return response


class AccessRecordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AccessRecord.objects.all()
    serializer_class = AccessRecordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AccessRecordUserList(APIView):
    def get(self, request, *args, **kwargs):
        access_record = AccessRecord.objects.filter(user_id=kwargs["user_id"])
        serializer = AccessRecordSerializer(access_record, many=True)
        return Response(serializer.data)
