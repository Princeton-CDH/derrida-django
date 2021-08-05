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


class Command(BaseCommand):
    '''Export reference data for each Derrida Work as CSV and JSON'''
    help = __doc__

    #: fields for CSV output
    csv_fields = [
        'id', 'item_type', 'work_title', 'work_short_title',
        'alternate_title', 'work_year', 'copyright_year',
        'print_date', 'work_authors', 'publisher', 'pub_place',
        'is_extant', 'is_annotated', 'is_translation', 'has_dedication',
        'has_insertions',
        # 'copy',
        # 'dimensions',
        # 'work_uri',
        # 'work_subjects',
        # 'languages',
        # 'journal_title',
        # 'book_title',
        # 'book_title_uri',
        # 'start_page',
        # 'end_page',
        # 'has_digital_edition',
        # 'uri',
        # 'zotero_id'

    # is_extant
    # is_annotated
    # is_translation
    # has_dedication
    # has_insertions
    # copy
    # dimensions
    # work_uri
    # work_subjects
    # languages
    # journal_title: instance.journal.name
    # book_title: instance.collected_in.display_title
    # book_title_uri: instance.collected_in.
    # start_page
    # end_page
    # has_digital_edition
    # uri [finding aid url: these almost certainly don't resolve anymore! can we get help from PUL to get catalog links for the same items?]
    # zotero_id (for compatibility with previous dataset)

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
            json.dump(instancedata, jsonfile, indent=2)

        # generate CSV export
        with open('{}.csv'.format(base_filename), 'w') as csvfile:
            # write utf-8 byte order mark at the beginning of the file
            csvfile.write(codecs.BOM_UTF8.decode())

            csvwriter = csv.DictWriter(csvfile, fieldnames=self.csv_fields)
            csvwriter.writeheader()

            for instance in instancedata:
                csvwriter.writerow(self.flatten_dict(instance))

    def instance_data(self, instance):
        '''Generate a dictionary of data to export for a single
         :class:`~derrida.books.models.Instance` object'''
        return OrderedDict([
            ('id', instance.get_uri()),
            ('item_type', instance.item_type),
            ('work_title', instance.work.primary_title),
            ('work_short_title', instance.work.short_title),
            ('alternate_title', instance.alternate_title),
            ('work_year', instance.work.year),
            ('copyright_year', instance.copyright_year),
            ('print_date', str(instance.print_date) if instance.print_date else ''),
            ('work_authors', [str(author) for author in instance.work.authors.all()]),
            ('publisher', instance.publisher.name if instance.publisher else ''),
            ('pub_place', [place.name for place in instance.pub_place.all()]),
            ('is_extant', instance.is_extant),
            ('is_annotated', instance.is_annotated),
            ('is_translation', instance.is_translation),
            ('has_dedication', instance.has_dedication),
            ('has_insertions', instance.has_insertions),
        ])



    # NOTE: This is the same for both, should I just call the other one?
    #  Should we centralize? Is it even worth it at this point?
    def flatten_dict(self, data):
        '''Flatten a dictionary with nested dictionaries or lists into a
        key value pairs that can be output as CSV.  Nested dictionaries will be
        flattened and keys combined; lists will be converted into semi-colon
        delimited strings.'''
        flat_data = {}
        for key, val in data.items():
            # for a nested subdictionary, combine key and nested key
            if isinstance(val, dict):
                for subkey, subval in val.items():
                    flat_data[' '.join([key, subkey])] = subval
            # convert list to a delimited string
            elif isinstance(val, list):
                flat_data[key] = ';'.join(val)
            else:
                flat_data[key] = val

        return flat_data
