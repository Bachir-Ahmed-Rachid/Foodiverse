# Generated by Django 4.2 on 2023-05-12 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendors", "0002_alter_vendor_user_alter_vendor_user_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="vendor",
            name="slug",
            field=models.SlugField(blank=True, max_length=150),
        ),
    ]
