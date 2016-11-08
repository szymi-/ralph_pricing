# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-04 13:23
from __future__ import unicode_literals

import sys

from django.db import migrations, models
from django.utils.text import slugify


def fill_base_usage_symbol(apps, schema_editor):
    BaseUsage = apps.get_model('ralph_scrooge', 'BaseUsage')
    for bu in BaseUsage._default_manager.filter(symbol=''):
        bu.symbol = slugify(bu.name)
        print('Saving symbol of {} to {}'.format(bu.name, bu.symbol))
        bu.save()


def check_base_usage_symbol_uniqueness(apps, schema_editor):
    BaseUsage = apps.get_model('ralph_scrooge', 'BaseUsage')
    duplicated_symbols = [
        s[0] for s in BaseUsage._default_manager.values_list('symbol').annotate(
            c=models.Count('id')
        ).filter(c__gt=1)
    ]
    if duplicated_symbols:
        print('\nMultiple base usage types with symbols:')
        print('\n'.join(duplicated_symbols))
        print('Fix them (make them unique) before applying this migration')
        sys.exit(1)


class Migration(migrations.Migration):

    dependencies = [
        ('ralph_scrooge', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            fill_base_usage_symbol,
            reverse_code=migrations.RunPython.noop
        ),
        migrations.RunPython(
            check_base_usage_symbol_uniqueness,
            reverse_code=migrations.RunPython.noop
        ),
        migrations.AlterField(
            model_name='baseusage',
            name='symbol',
            field=models.CharField(blank=True, default='', editable=False, help_text='(Usually) slug of the name of the usage. Used (mostly) in API to specify type of the usage.', max_length=255, unique=True, verbose_name='symbol'),
        ),
    ]
