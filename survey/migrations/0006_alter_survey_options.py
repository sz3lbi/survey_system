# Generated by Django 3.2.4 on 2021-06-14 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_auto_20210614_1806'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='survey',
            options={'permissions': (('view_list', 'Can see survey list \\w questions and available answers'), ('view_stats', 'Can see statistics on surveys'))},
        ),
    ]