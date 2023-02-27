# Generated by Django 4.1.7 on 2023-02-24 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0005_rename_classroomname_exam_classroom'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='examname',
            new_name='exam',
        ),
        migrations.RenameField(
            model_name='option',
            old_name='optionname',
            new_name='option',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='Questionname',
            new_name='question',
        ),
        migrations.AlterField(
            model_name='classroom',
            name='standard',
            field=models.IntegerField(),
        ),
    ]
