# Generated by Django 4.1.7 on 2023-02-24 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_account_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('studentuser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='account.account')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('Teacheruser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='account.account')),
            ],
        ),
    ]
