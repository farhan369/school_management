# Generated by Django 4.1.7 on 2023-03-29 09:28

import academics.constants
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("academics", "0006_alter_classroom_division"),
    ]

    operations = [
        migrations.AlterField(
            model_name="classroom",
            name="division",
            field=models.IntegerField(
                blank=True,
                default=academics.constants.Divisions["A"],
                verbose_name=(
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
                ),
            ),
        ),
    ]
