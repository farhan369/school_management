# Generated by Django 4.1.7 on 2023-02-24 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_alter_try_tryno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='class_limit',
            field=models.IntegerField(blank=True, default=2, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='event',
            field=models.CharField(blank=True, default=None, max_length=25),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.IntegerField(blank=True, choices=[(0, 'Time'), (1, 'Distance')], default=0, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sportsfestival',
            name='from_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sportsfestival',
            name='to_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='try',
            name='result',
            field=models.IntegerField(blank=True, default=2, null=True),
        ),
        migrations.AlterField(
            model_name='try',
            name='tryno',
            field=models.IntegerField(blank=True, default=2, null=True),
        ),
    ]
