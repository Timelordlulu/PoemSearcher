# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-08-15 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='poem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('writer', models.CharField(max_length=30)),
                ('content', models.CharField(max_length=500)),
            ],
        ),
    ]