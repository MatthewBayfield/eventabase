# Generated by Django 4.1 on 2022-10-23 18:07

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='address_line_one',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(flags=re.RegexFlag['MULTILINE'], message='Must contain only standard alphabetic characters and numbers, with single spaces between words.', regex='^([a-zA-Z0-9]+\\s{0,1}[a-zA-Z0-9]+)+\\Z'), django.core.validators.MaxLengthValidator(100)], verbose_name='Address line 1'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='city_or_town',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Must contain only standard alphabetic characters, with single spaces between words.', regex='^([a-zA-Z]+\\s{0,1}[a-zA-Z]+)+\\Z'), django.core.validators.MaxLengthValidator(50)], verbose_name='City/Town'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='county',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Must contain only standard alphabetic characters, with single spaces between words.', regex='^([a-zA-Z]+\\s{0,1}[a-zA-Z]+)+\\Z'), django.core.validators.MaxLengthValidator(50)], verbose_name='County'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='postcode',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Must be a valid postcode format.', regex='^(([gG][iI][rR] {0,}0[aA]{2})|((([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y]?[0-9][0-9]?)|(([a-pr-uwyzA-PR-UWYZ][0-9][a-hjkstuwA-HJKSTUW])|([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y][0-9][abehmnprv-yABEHMNPRV-Y]))) {0,}[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2}))$'), django.core.validators.MaxLengthValidator(10)], verbose_name='Postcode'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(flags=re.RegexFlag['IGNORECASE'], message='Must contain only standard alphabetic characters.', regex='^[A-Za-z]+$'), django.core.validators.MaxLengthValidator(50)], verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(flags=re.RegexFlag['IGNORECASE'], message='Must contain only standard alphabetic characters.', regex='^[A-Za-z]+$'), django.core.validators.MaxLengthValidator(50)], verbose_name='last name'),
        ),
    ]