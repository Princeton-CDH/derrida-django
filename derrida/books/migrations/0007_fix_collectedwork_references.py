# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-01 21:51
from __future__ import unicode_literals

from django.db import migrations


def fix_collectedwork_references(apps, schema_editor):
    Instance = apps.get_model('books', 'Instance')

    # find works that collect other works and have references
    for instance in Instance.objects.filter(collected_set__isnull=False) \
                                    .filter(reference__isnull=False) \
                                    .distinct():
        # collect start and end pages for book sections
        sections = []
        for bksection in instance.collected_set.filter(start_page__isnull=False) \
                                               .filter(end_page__isnull=False).all():
            # convert pages to integer for comparison
            sections.append((int(bksection.start_page), int(bksection.end_page), bksection))

        # sort sections by start page number
        sections.sort(key=lambda tup: tup[0])

        # look through references that have page numbers
        # and associate with appropriate section
        for ref in instance.reference_set.exclude(book_page__exact=''):
            # handle page range or single page
            if '-' in ref.book_page:
                start, end = [int(page.rstrip('ps')) for page in ref.book_page.split('-')]
            else:
                start = end = int(ref.book_page.rstrip('ps'))
            # find the section this page or page range belongs to
            for section_start, section_end, booksection in sections:
                if start >= section_start and end <= section_end:
                    # reassociate reference with this section of the book
                    ref.instance = booksection
                    ref.save()
                    break


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_suppress_images_fields'),
    ]

    operations = [
        migrations.RunPython(
            code=fix_collectedwork_references,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
