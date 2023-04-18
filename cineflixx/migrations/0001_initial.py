# Generated by Django 4.1 on 2023-04-17 22:49

import cineflixx.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Movie",
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
                ("name", models.CharField(max_length=100, unique=True)),
                ("protagonists", models.CharField(max_length=100)),
                ("start_date", models.DateTimeField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("coming-up", "Coming Up"),
                            ("starting", "Starting"),
                            ("running", "Running"),
                            ("finished", "Finished"),
                        ],
                        default="coming-up",
                        max_length=20,
                    ),
                ),
                ("ranking", models.IntegerField(default=0)),
                (
                    "poster",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=cineflixx.models.poster_dir_path,
                    ),
                ),
            ],
        ),
    ]
