# Generated by Django 3.2.4 on 2021-06-26 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_survey_name_pl'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='text_en',
            field=models.CharField(max_length=16, null=True, unique=True, verbose_name='text'),
        ),
        migrations.AddField(
            model_name='answer',
            name='text_pl',
            field=models.CharField(max_length=16, null=True, unique=True, verbose_name='text'),
        ),
        migrations.AddField(
            model_name='question',
            name='text_en',
            field=models.CharField(max_length=64, null=True, unique=True, verbose_name='text'),
        ),
        migrations.AddField(
            model_name='question',
            name='text_pl',
            field=models.CharField(max_length=64, null=True, unique=True, verbose_name='text'),
        ),
    ]
