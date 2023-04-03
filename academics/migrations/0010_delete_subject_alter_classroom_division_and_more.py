# Generated by Django 4.1.7 on 2023-03-30 04:00

import academics.constants
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0006_alter_account_user_type"),
        ("academics", "0009_subject_classroom_academic_year_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Subject",
        ),
        migrations.AlterField(
            model_name="classroom",
            name="division",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (101, "A"),
                    (102, "B"),
                    (103, "C"),
                    (104, "D"),
                    (105, "E"),
                    (106, "F"),
                    (107, "G"),
                    (108, "H"),
                    (109, "I"),
                    (110, "J"),
                    (111, "K"),
                    (112, "L"),
                    (113, "M"),
                    (114, "N"),
                    (115, "O"),
                    (116, "P"),
                    (117, "Q"),
                    (118, "R"),
                    (119, "S"),
                    (120, "T"),
                    (121, "U"),
                    (122, "V"),
                    (123, "W"),
                    (124, "X"),
                    (125, "Y"),
                    (126, "Z"),
                ],
                default=academics.constants.Divisions["A"],
            ),
        ),
        migrations.AlterField(
            model_name="classroom",
            name="teacher",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="classroom",
                to="account.teacher",
            ),
        ),
    ]