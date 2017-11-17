# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-08-23 14:32
from __future__ import unicode_literals

import re
import sys
from unidecode import unidecode
import django.core.validators
from django.db import migrations, models
from django.db.transaction import atomic
from django.utils.text import slugify


def generate_base_slug(obj):
    '''Generate slug for :class:`~derrida.books.models.Instance` object.
       Copy of method to make avail in migration.

       :param obj: Object of :class:`~derrida.books.models.Instance`
       :rtype str: String in the format ``lastname-title-of-work-year``
    '''
    # get the first author, if there is one, by authorized name
    author = obj.work.authors.order_by('authorized_name').first()
    if author:
        # use the last name of the first author
        author = author.authorized_name.split(',')[0]
    else:
        # otherwise, set it to an empty string
        author = ''
    # first 10 words
    title = ' '.join(obj.work.primary_title.split()[0:9])
    year = obj.copyright_year
    # if no instance copyright_year,
    if not year:
        # try the work year,
        year = obj.work.year
    if not year:
        # if still no year, use blank string
        year = ''
    # return a slug with no distinction for copies
    return slugify('%s %s %s' % (author, unidecode(title), year))


def add_slugs(apps, schema_editor):
    '''Add slugs to models as part of migration'''
    Instance = apps.get_model('books', 'Instance')

    @atomic
    def update_instances(obj_list):
        '''Iterate over objects in the obj_list and save atomically'''
        for item in obj_list:
            item.save()

    # convert SELECT * query set into list
    instances = list(Instance.objects.all())

    # give them all base slugs
    for instance in instances:
        instance.slug = generate_base_slug(instance)

    # - validate them and add characters to duplicates
    # sort by slug so any repeated slugs will show up together
    instances = sorted(instances, key=lambda instance: instance.slug)

    # loop through, tracking previous item to check for dupes
    prev_item = None
    prev_slug = None
    for item in instances:
        if prev_slug and item.slug == prev_slug:
            # if previous item does not have a copy letter,
            # set it now starting with A
            if not prev_item.copy:
                prev_item.copy = 'A'
                # update slug to include copy letter and make unique
                prev_item.slug = '%s-%s' % (prev_item.slug, prev_item.copy)

            # current item gets the next letter
            item.copy = chr(ord(prev_item.copy) + 1)
            # update slug to include copy letter and make unique
            item.slug = '%s-%s' % (item.slug, item.copy)

            # current item becomes previous for differentiating letters
            prev_item = item
            # preserve generic slug for comparison

        else:
            # no duplicate detected; item and slug become next previous
            prev_item = item
            prev_slug = item.slug

    # save all the updated instances
    update_instances(instances)


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_derridawork_section_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='derridaworksection',
            options={'ordering': ['derridawork', 'order']},
        ),
        migrations.AddField(
            model_name='instance',
            name='slug',
            field=models.SlugField(unique=False, blank=True, help_text='Editing this after a record is created should be done with caution as it will break the previous URL.', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='instance',
            name='copy',
            field=models.CharField(blank=True, help_text='Label to distinguish multiple copies of the same edition', max_length=1, validators=[django.core.validators.RegexValidator('[A-Z]', message='Please set a capital letter from A-Z.')]),
        ),
        # Make the slugs and validate their uniqueness
        migrations.RunPython(
            code=add_slugs,
            reverse_code=migrations.RunPython.noop,
        ),
        # Alter the field to make it SlugField with max_length 255
        migrations.AlterField(
            model_name='instance',
            name='slug',
            field=models.SlugField(
                blank=False,
                unique=True,
                max_length=255,
                help_text='Editing this after a record is created should be done with caution as it will break the previous URL.',
            ),
        ),
    ]
