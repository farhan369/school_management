# Generated by Django 4.1.7 on 2023-03-02 12:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("academics", "0011_alter_classroom_teacher_alter_exam_classroom_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="exam",
            old_name="exam",
            new_name="name",
        ),
        migrations.RenameField(
            model_name="option",
            old_name="option",
            new_name="text",
        ),
        migrations.RenameField(
            model_name="question",
            old_name="question",
            new_name="text",
        ),
    ]