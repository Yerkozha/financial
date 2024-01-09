# Generated by Django 5.0 on 2024-01-08 15:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_notes_appointmentmodel_summary_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointmentmodel',
            name='appointment_date',
        ),
        migrations.AddField(
            model_name='appointmentmodel',
            name='color',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointmentmodel',
            name='end',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='appointmentmodel',
            name='start',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]