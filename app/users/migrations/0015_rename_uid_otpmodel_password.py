# Generated by Django 5.0 on 2024-12-30 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_otpmodel_individualmodel_is_phone_verified_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otpmodel',
            old_name='uid',
            new_name='password',
        ),
    ]
