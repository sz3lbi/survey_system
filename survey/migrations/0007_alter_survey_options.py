# Generated by Django 3.2.4 on 2021-06-21 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_alter_survey_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='survey',
            options={'permissions': (('view_stats', 'Can see statistics on surveys'),)},
        ),
    ]
