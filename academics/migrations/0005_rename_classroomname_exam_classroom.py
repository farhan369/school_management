# Generated by Django 4.1.7 on 2023-02-24 06:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("academics", "0004_alter_classroom_standard"),
    ]

    operations = [
        migrations.RenameField(
            model_name="exam",
            old_name="classroomname",
            new_name="classroom",
        ),
    ]
