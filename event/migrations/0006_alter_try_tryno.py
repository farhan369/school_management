# Generated by Django 4.1.7 on 2023-02-24 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_rename_event_registration_eventregistration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='try',
            name='tryno',
            field=models.IntegerField(),
        ),
    ]
