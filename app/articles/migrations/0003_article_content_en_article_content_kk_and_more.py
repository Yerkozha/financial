# Generated by Django 5.0 on 2024-03-05 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_create_date_article_modified_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='content_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='content_kk',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='content_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='title_en',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='title_kk',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='title_ru',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
