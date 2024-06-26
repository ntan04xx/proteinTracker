# Generated by Django 5.0.5 on 2024-06-07 06:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calorie_count", "0003_userlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="userlist",
            name="calorie_target",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="userlist",
            name="fat_target",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="userlist",
            name="protein_target",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="userlist",
            name="timestamp",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
