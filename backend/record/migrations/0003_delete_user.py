# Generated by Django 4.1.3 on 2022-12-04 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("record", "0002_alter_accessrecord_check_time_alter_dailyrecord_date"),
    ]

    operations = [
        migrations.DeleteModel(
            name="User",
        ),
    ]
