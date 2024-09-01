# Generated by Django 4.2.15 on 2024-08-30 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Disease",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("problem_name", models.CharField(max_length=100, unique=True)),
                ("time_required", models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name="RoomAllotment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "room_type",
                    models.CharField(
                        choices=[
                            ("ICU", "ICU"),
                            ("General", "General"),
                            ("Private", "Private"),
                        ],
                        max_length=30,
                    ),
                ),
                ("allotment_date", models.DateField(blank=True, null=True)),
                ("discharge_date", models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Specialization",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("specialization_name", models.CharField(max_length=100)),
            ],
        ),
    ]
