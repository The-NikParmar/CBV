# Generated by Django 5.1 on 2024-08-31 11:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0007_alter_appointment_appointment_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(seconds=1800)),
        ),
    ]
