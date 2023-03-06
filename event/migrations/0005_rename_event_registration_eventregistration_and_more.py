# Generated by Django 4.1.7 on 2023-02-24 10:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0006_rename_studentuser_student_user_and_more"),
        ("event", "0004_alter_event_event_type_alter_try_result_tryno"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Event_registration",
            new_name="EventRegistration",
        ),
        migrations.RenameModel(
            old_name="Sports_festival",
            new_name="SportsFestival",
        ),
        migrations.RenameModel(
            old_name="Try_result",
            new_name="Try",
        ),
        migrations.RenameField(
            model_name="event",
            old_name="eventname",
            new_name="event",
        ),
        migrations.RenameField(
            model_name="sportsfestival",
            old_name="festname",
            new_name="fest",
        ),
    ]
