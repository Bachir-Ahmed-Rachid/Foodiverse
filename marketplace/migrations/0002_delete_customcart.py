# Generated by Django 4.2 on 2023-05-17 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("marketplace", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="CustomCart",
        ),
    ]