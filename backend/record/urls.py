from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("daily/", views.DailyRecordList.as_view()),
    path("daily/<int:pk>/", views.DailyRecordDetail.as_view()),
    path("daily/user/<int:user_id>/", views.DailyRecordUserList.as_view()),
    path("daily/today/", views.DailyRecordDetail.as_view()),
    path("access/", views.AccessRecordList.as_view()),
    path("access/<int:pk>/", views.AccessRecordDetail.as_view()),
    path("access/user/<int:user_id>/", views.AccessRecordUserList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
