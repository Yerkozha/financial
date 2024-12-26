# Generated by Django 5.0 on 2024-12-25 19:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_devicetoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('historical', 'Historical'), ('literature', 'Literature'), ('science', 'Science'), ('poetry', 'Poetry')], default='literature', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('published_date', models.DateField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('book_file', models.FileField(blank=True, null=True, upload_to='books/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.author')),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('genres', models.ManyToManyField(to='users.genre')),
            ],
        ),
        migrations.CreateModel(
            name='AIInsights',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.TextField(blank=True, null=True)),
                ('sentiment', models.JSONField(blank=True, null=True)),
                ('keywords', models.JSONField(blank=True, null=True)),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ai_insights', to='users.book')),
            ],
        ),
        migrations.CreateModel(
            name='BookMetadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField()),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.book')),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('order', models.PositiveIntegerField()),
                ('content', models.TextField()),
                ('annotations', models.JSONField(default=dict)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='users.book')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by', to='users.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Paragraph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('text', models.TextField()),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paragraphs', to='users.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessedContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tokenized', models.JSONField(blank=True, null=True)),
                ('embeddings', models.JSONField(blank=True, null=True)),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='processed_content', to='users.book')),
            ],
        ),
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['title'], name='users_book_title_a531e2_idx'),
        ),
    ]
