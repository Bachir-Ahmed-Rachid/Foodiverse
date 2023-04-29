# Generated by Django 4.2 on 2023-04-28 21:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
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
                    "profile_picture",
                    models.ImageField(
                        blank=True, null=True, upload_to="user/profile_picture"
                    ),
                ),
                (
                    "cover_picture",
                    models.ImageField(
                        blank=True, null=True, upload_to="user/cover_picture"
                    ),
                ),
                (
                    "address_line_1",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "address_line_2",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("country", models.CharField(blank=True, max_length=50, null=True)),
                ("state", models.CharField(blank=True, max_length=50, null=True)),
                ("city", models.CharField(blank=True, max_length=50, null=True)),
                ("pin_code", models.CharField(blank=True, max_length=6, null=True)),
                ("latitude", models.CharField(blank=True, max_length=6, null=True)),
                ("longitude", models.CharField(blank=True, max_length=6, null=True)),
                ("created_at", models.DateField(auto_now_add=True)),
                ("modified_at", models.DateField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
