# Generated by Django 5.0 on 2024-12-30 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_rename_uid_otpmodel_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualmodel',
            name='is_phone_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='individualmodel',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]
