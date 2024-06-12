# Generated by Django 5.0.5 on 2024-06-12 10:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calorie_count", "0008_remove_userdetails_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="userdetails",
            name="user",
            field=models.OneToOneField(
                default=25,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_details",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
