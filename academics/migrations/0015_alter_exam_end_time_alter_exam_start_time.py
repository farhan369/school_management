# Generated by Django 4.1.7 on 2023-03-31 08:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("academics", "0014_alter_academicyear_end_year_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exam",
            name="end_time",
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="exam",
            name="start_time",
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
