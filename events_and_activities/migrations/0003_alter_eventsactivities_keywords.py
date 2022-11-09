# Generated by Django 4.1 on 2022-10-29 01:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_and_activities', '0002_alter_eventsactivities_keywords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventsactivities',
            name='keywords',
            field=models.CharField(blank=True, max_length=75, validators=[django.core.validators.MaxLengthValidator(75), django.core.validators.RegexValidator(message='Must contain comma separated words containing only the characters [a-zA-Z0-9_], with no spaces.', regex='^([a-zA-Z0-9]+,{1})+[a-zA-Z0-9]+')]),
        ),
    ]