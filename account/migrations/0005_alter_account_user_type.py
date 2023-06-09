# Generated by Django 4.1.7 on 2023-03-29 09:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0004_alter_account_user_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="user_type",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[(1, "student"), (2, "teacher"), (3, "admin")],
                default=None,
            ),
        ),
    ]
