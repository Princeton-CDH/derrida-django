'''
Manage command to export instance data.

Takes an optional argument to specify the output directory. Otherwise,
files are created in the current directory.
'''

import codecs
from collections import OrderedDict
import csv
import json
import os.path

from django.core.management.base import BaseCommand

from derrida.books.models import Instance
from derrida.books.management.commands import reference_data


class Command(reference_data.Command):
    '''Export reference data for each Derrida Work as CSV and JSON'''
    help = __doc__

    #: fields for CSV output
    csv_fields = [
        'id', 'item_type', 'title', 'short_title',
        'alternate_title', 'work_year', 'copyright_year',
        # TODO: take into account print date day/month/year known fields
        # 'print_date', 
        'authors', 'publisher', 'pub_place',
        'is_extant', 'is_annotated', 'is_translation', 'has_dedication',
        'has_insertions', 'copy', 'dimensions', 'work_uri',
        'subjects', 'languages', 'journal_title',
        'book_title', 'book_title_uri',
        'start_page', 'end_page',
        'has_digital_edition', 'catalog_uri', 'zotero_id'
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '-d', '--directory',
            help='Specify the directory where files should be generated')

    def handle(self, *args, **kwargs):
        base_filename = 'derrida-instance-data'
        if kwargs['directory']:
            base_filename = os.path.join(kwargs['directory'], base_filename)

        instancedata = [self.instance_data(instance) for instance in Instance.objects.filter(cited_in__isnull=False)]

        # list of dictionaries can be output as is for JSON export
        with open('{}.json'.format(base_filename), 'w') as jsonfile:
            json_instancedata = [{field: inst[field] for field in inst.keys() if inst[field] not in [None, '', []]} for inst in instancedata]
            json.dump(json_instancedata, jsonfile, indent=2)

        # generate CSV export
        with open('{}.csv'.format(base_filename), 'w') as csvfile:
            # write utf-8 byte order mark at the beginning of the file
            csvfile.write(codecs.BOM_UTF8.decode())

            csvwriter = csv.DictWriter(csvfile, fieldnames=self.csv_fields)
            csvwriter.writeheader()

            for instance in instancedata:
                csvwriter.writerow(self.flatten_dict(instance))

    def update_findingaids_url(self, old_url):
        # Structure of the URL changed after the findingaids site updated.
        if 'findingaids.princeton.edu' not in old_url:
            return old_url
        
        new_url = old_url.replace('http:', 'https:')
        new_url = new_url.split('?', 1)[0]
        new_url = new_url.replace('/collections/', '/catalog/')

        # manipulate changes to item slug
        splitter = '/catalog/'
        base_url, item_slug = new_url.split(splitter)
        item_slug = item_slug.replace('/', '_')
        item_slug = item_slug.replace('.', '-')

        return base_url + splitter + item_slug

    def collect_all_languages(self, instance):
        if instance.work:
            return list(set([str(lang) for lang in instance.work.languages.all()] + [str(lang) for lang in instance.languages.all()]))
        else:
            return [str(lang) for lang in instance.languages.all()] 

    def instance_data(self, instance):
        '''Generate a dictionary of data to export for a single
         :class:`~derrida.books.models.Instance` object'''

        return OrderedDict([
            ('id', instance.get_uri()),
            ('item_type', instance.item_type),
            ('title', instance.work.primary_title),
            ('short_title', instance.work.short_title),
            ('alternate_title', instance.alternate_title),
            ('work_year', instance.work.year),
            ('copyright_year', instance.copyright_year),
            # TODO: take into account print date day/month/year known fields
            # ('print_date', str(instance.print_date) if instance.print_date else ''),
            ('authors', [str(author) for author in instance.work.authors.all()]),
            ('publisher', instance.publisher.name if instance.publisher else ''),
            ('pub_place', [place.name for place in instance.pub_place.all()]),
            ('is_extant', instance.is_extant),
            ('is_annotated', instance.is_annotated),
            ('is_translation', instance.is_translation),
            ('has_dedication', instance.has_dedication),
            ('has_insertions', instance.has_insertions),
            ('copy', instance.copy),
            ('work_uri', instance.work.uri),
            ('subjects', [str(subject) for subject in instance.work.subjects.all()]),
            ('languages', self.collect_all_languages(instance)),
            ('journal_title', instance.journal.name if instance.journal else ''),
            ('book_title', instance.collected_in.display_title() if instance.collected_in else ''),
            ('book_title_uri', instance.collected_in.get_uri() if instance.collected_in else ''),
            ('start_page', instance.start_page),
            ('end_page', instance.end_page),
            ('has_digital_edition', bool(instance.digital_edition)),
            ('catalog_uri', self.update_findingaids_url(instance.uri)),
            ('zotero_id', instance.zotero_id),
        ])
