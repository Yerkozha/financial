# Generated by Django 5.0 on 2023-12-10 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='financial',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='financial',
            name='bank_vtorogo_urovnya',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='financial',
            name='bankovskie_holdingi',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='financial',
            name='bin',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='financial',
            name='chleny_pravleniya',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financial',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='financial',
            name='fax',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='financial',
            name='glavnyy_buhgalter',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financial',
            name='kastodian',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='financial',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='financial',
            name='predsedatel_pravleniya',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financial',
            name='sovet_direktorov',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='financial',
            name='predsedatelSovetaDirektorov',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
