# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-18 09:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bibliosoft', '0004_auto_20181018_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fine',
            name='list_id',
            field=models.AutoField(max_length=32, primary_key=True, serialize=False),
        ),
    ]