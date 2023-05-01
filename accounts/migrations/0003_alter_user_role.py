# Generated by Django 4.2 on 2023-05-01 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_userprofile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.PositiveSmallIntegerField(
                blank=True, choices=[(1, "VENDOR"), (2, "CUSTOMER")], null=True
            ),
        ),
    ]
