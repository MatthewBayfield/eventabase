# Generated by Django 4.1.3 on 2022-11-03 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events_and_activities', '0005_alter_eventsactivities_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventsactivities',
            options={'ordering': ['-closing_date'], 'verbose_name': 'Events and Activities', 'verbose_name_plural': 'Events and Activities'},
        ),
    ]