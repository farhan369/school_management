# Generated by Django 4.1.7 on 2023-02-24 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0007_alter_classroom_division_alter_classroom_standard_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
