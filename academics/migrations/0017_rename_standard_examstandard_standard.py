# Generated by Django 4.1.7 on 2023-03-31 10:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("academics", "0016_rename_end_time_exam_end_date_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="examstandard",
            old_name="Standard",
            new_name="standard",
        ),
    ]
