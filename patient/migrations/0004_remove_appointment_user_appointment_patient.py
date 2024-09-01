# Generated by Django 4.2.15 on 2024-08-30 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("patient", "0003_appointment_doctor"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="appointment",
            name="user",
        ),
        migrations.AddField(
            model_name="appointment",
            name="patient",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="patient.patient",
            ),
            preserve_default=False,
        ),
    ]
