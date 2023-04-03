# Generated by Django 4.1.7 on 2023-03-30 08:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("academics", "0012_academicyear_examstandard_standard_subject_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="academicyear",
            old_name="year",
            new_name="start_year",
        ),
        migrations.AddField(
            model_name="academicyear",
            name="end_year",
            field=models.IntegerField(blank=True, default=2020),
        ),
    ]
