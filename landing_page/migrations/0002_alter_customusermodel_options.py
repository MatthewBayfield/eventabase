# Generated by Django 4.1 on 2022-10-30 02:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing_page', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customusermodel',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]
