# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-08 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_fix_collectedwork_references'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='slug',
            field=models.SlugField(blank=True, help_text='To auto-generate a valid slug for a new instance, choose a work then click "Save and Continue Editing" in the lower right. Editing slugs of previously saved instances should be done with caution, as this may break permanent links.', max_length=255, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='instance',
            unique_together=set([('work', 'copyright_year', 'copy')]),
        ),
    ]
