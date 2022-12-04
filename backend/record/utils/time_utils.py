from datetime import datetime, time, timedelta
from django.utils import timezone

# 하루 기준 : 오전 6시
def working_timezone(base_time=timezone.now()):
    today_min = datetime.combine(base_time.date(), time(hour=6))
    today_max = datetime.combine(base_time.date() + timedelta(days=1), time(hour=6))
    if today_min < base_time < today_max:
        return base_time.date()
    else:
        return base_time.date() - timedelta(1)
