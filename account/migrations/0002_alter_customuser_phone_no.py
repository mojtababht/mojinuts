# Generated by Django 4.2.1 on 2023-06-05 14:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_no',
            field=models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be in the format: '0999999999'. Up to 11 digits allowed.", regex='^\\+?1?\\d{9,11}$')]),
        ),
    ]
