from record.models import DailyRecord, AccessRecord
from django.utils import timezone
from datetime import datetime, time, timedelta
from .time_utils import *

DAILY_OFFSET = 1
ACCESS_OFFSET = 2


def record_daily(data):
    if is_record_now(data):
        record_daily_now(data)
    else:
        record_daily_previous(data)


def record_daily_previous(data):
    record_time = datetime.fromisoformat(data["check_time"])
    access_record = load_access_record(data, record_time)
    daily_record = load_daily_record(data, record_time)
    find_index = binary_search(record_time, access_record)
    # 출근 기록인 경우
    if find_index == 0 and access_record[find_index]["tag"] == "IN":
        if daily_record:
            daily_record.go_time = data["check_time"]
            daily_record.save()
        else:
            record = DailyRecord(user_id=data["user_id"], date=record_time, go_time=data["check_time"])
            record.save()
    # 퇴근 기록인 경우
    elif find_index + 1 == len(access_record) and access_record[find_index]["tag"] == "OUT":
        daily_record.leave_time = data["check_time"]
        daily_record.save()
    # 해당 시간 이전에 기록이 있는 경우
    if find_index - 1 > 0:
        if access_record[find_index - 1]["tag"] == "IN" and access_record[find_index]["tag"] == "OUT":
            checking_time = int((access_record[find_index]["check_time"] - access_record[find_index - 1]["check_time"]).total_seconds() // 60)
            daily_record.working_time += checking_time
            daily_record.save()
        elif access_record[find_index - 1]["tag"] == "OUT" and access_record[find_index]["tag"] == "IN":
            checking_time = int((access_record[find_index]["check_time"] - access_record[find_index - 1]["check_time"]).total_seconds() // 60)
            daily_record.break_time += checking_time
            daily_record.save()
    # 해당 시간 이후에 기록이 있는 경우
    if find_index + 1 < len(access_record):
        if access_record[find_index]["tag"] == "IN" and access_record[find_index + 1]["tag"] == "OUT":
            checking_time = int((access_record[find_index + 1]["check_time"] - access_record[find_index]["check_time"]).total_seconds() // 60)
            daily_record.working_time += checking_time
            daily_record.save()
        elif access_record[find_index]["tag"] == "OUT" and access_record[find_index + 1]["tag"] == "IN":
            checking_time = int((access_record[find_index + 1]["check_time"] - access_record[find_index]["check_time"]).total_seconds() // 60)
            daily_record.break_time += checking_time
            daily_record.save()


def record_daily_now(data):
    access_record = load_access_record(data)
    daily_record = load_daily_record(data)
    if data["tag"] == "IN":
        if access_record and daily_record and len(access_record) >= 2:
            if list(access_record)[len(access_record) - 2]["tag"] == "OUT":
                break_time = check_inout_time_minute(access_record, ACCESS_OFFSET)
                daily_record.break_time += break_time
                daily_record.save()
        else:
            record = DailyRecord(user_id=data["user_id"])
            record.save()
    elif data["tag"] == "OUT":
        if access_record and daily_record and len(access_record) >= 2:
            if list(access_record)[len(access_record) - 2]["tag"] == "IN":
                working_time = check_inout_time_minute(access_record, ACCESS_OFFSET)
                daily_record.working_time += working_time
            daily_record.leave_time = timezone.now()
            daily_record.save()
        else:
            record = DailyRecord(user_id=data["user_id"], leave_time=timezone.now())
            record.save()


def binary_search(target, record):
    left = 0
    right = len(record) - 1
    mid = 0
    while left <= right:
        mid = (left + right) // 2
        if record[mid]["check_time"] == target:
            return mid
        elif record[mid]["check_time"] > target:
            right = mid - 1
        else:
            left = mid + 1
    return mid


def update_daily_now(data):
    for row in data:
        if row["date"] == str(timezone.now().date()):
            today_access = load_access_record(row)
            if list(today_access)[len(today_access) - DAILY_OFFSET]["tag"] == "IN":
                row["working_time"] = int(row["working_time"]) + check_inout_time_minute(today_access, DAILY_OFFSET)
    return data


def is_record_now(data):
    if data.get("check_time", False):
        return False
    return True


def get_daily_record_today(data):
    today_min = datetime.combine(timezone.now().date(), time(hour=6))
    today_max = datetime.combine(timezone.now().date() + timedelta(days=1), time(hour=6))
    today_access = AccessRecord.objects.filter(user_id=data["user_id"], check_time__range=(today_min, today_max)).values()
    return today_access


def check_inout_time_minute(today_access, offset):
    checking_time = int((timezone.now() - list(today_access)[len(today_access) - offset]["check_time"]).total_seconds() // 60)
    return checking_time


def load_daily_record(data, date=timezone.now()):
    try:
        today_daily = DailyRecord.objects.get(user_id=data["user_id"], date=date)
    except:
        today_daily = None
    return today_daily


def load_access_record(data, date=timezone.now()):
    min_time = datetime.combine(date.date(), time(hour=6))
    max_time = datetime.combine(date.date() + timedelta(days=1), time(hour=6))
    access_record = AccessRecord.objects.filter(user_id=data["user_id"], check_time__range=(min_time, max_time)).order_by("check_time").values()
    return access_record


def is_record_future_time(data):
    if data.get("check_time", False):
        record_time = datetime.fromisoformat(data["check_time"])
        now_time = timezone.now()
        if now_time < record_time:
            return True
    return False


def is_record_previous_time(data):
    if data["check_time"]:
        record_time = datetime.fromisoformat(data["check_time"])
        now_time = timezone.now()
        if now_time > record_time:
            return True
    return False
