from django.contrib import admin
from .models import AccessRecord, DailyRecord

# Register your models here.
admin.site.register(AccessRecord)
admin.site.register(DailyRecord)
