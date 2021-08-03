'''
Manage command to export intervention data for use by others.

Generates a CSV and JSON file with details for all interventions
documented in the database.

Takes an optional argument to specify the output directory. Otherwise,
files are created in the current directory.

'''


import codecs
from collections import OrderedDict
import csv
import json
import os.path

from derrida.books.management.commands import reference_data
from derrida.interventions.models import Intervention


class Command(reference_data.Command):
    '''Export intervention data from the database as CSV and JSON'''
    help = __doc__

    # NOTE: extending reference_data manage command to inherit
    # flatten_data method; there is more overlap and these scripts
    # could probably be generalized further for re-use

    #: fields for CSV output
    csv_fields = [
        'id', 'book id', 'book title', 'book type', 'page', 'tags', 'text content',
        'text language', 'text language code', 'text translation',
        'quote content', 'quote language', 'quote language code', 'annotator'
    ]

    #: base filename, for CSV and JSON output
    base_filename = 'interventions'

    def add_arguments(self, parser):
        parser.add_argument(
            '-d', '--directory',
            help='Specify the directory where files should be generated')

    def handle(self, *args, **kwargs):

        if kwargs['directory']:
            self.base_filename = os.path.join(kwargs['directory'], self.base_filename)

        # aggregate intervention data to be exported for use in generating
        # CSV and JSON output
        data = [self.intervention_data(intervention)
                   for intervention in Intervention.objects.all()]

        # list of dictionaries can be output as is for JSON export
        with open('{}.json'.format(self.base_filename), 'w') as jsonfile:
            json.dump(data, jsonfile, indent=2)

        # generate CSV export
        with open('{}.csv'.format(self.base_filename), 'w') as csvfile:
            # write utf-8 byte order mark at the beginning of the file
            csvfile.write(codecs.BOM_UTF8.decode())

            csvwriter = csv.DictWriter(csvfile, fieldnames=self.csv_fields)
            csvwriter.writeheader()

            for intervention in data:
                csvwriter.writerow(self.flatten_dict(intervention))

    def intervention_data(self, intervention):
        '''Generate a dictionary of data to export for a single
        :class:`~derrida.books.models.Reference` object'''

        # NOTE: using OrderedDict to ensure JSON output follows logical
        # order in Python < 3.6, where dict order is not guaranteed

        data = OrderedDict([
            ('id', intervention.get_uri()),
            # every intervention *should* be associated with a book,
            # but possible that some are not
            ('book', OrderedDict([
                ('id', intervention.work_instance.get_uri() if intervention.work_instance else ''),
                ('title', intervention.work_instance.display_title() if intervention.work_instance else ''),
                ('type', intervention.work_instance.item_type if intervention.work_instance else '')
            ])),
            # canvas object *should* have a label, but possible it does not
            ('page', intervention.canvas.label if intervention.canvas else ''),
            ('tags', [tag.name for tag in intervention.tags.all()]),
            ('ink', ';'.join(intervention.ink)),
            ('page_iiif', str(intervention.canvas.image if intervention.canvas else '')),
            ('annotation_region', str(intervention.iiif_image_selection())),
        ])

        # only include text and quote information if we have content
        if intervention.text:
            text_info = OrderedDict({
                'content': intervention.text
            })
            if intervention.text_language:
                text_info['language'] = intervention.text_language.name
                text_info['language code'] = intervention.text_language.code
            if intervention.text_translation:
                text_info['translation'] = intervention.text_translation

            data['text'] = text_info

        if intervention.quote:
            quote_info = OrderedDict({
                'content': intervention.quote
            })
            if intervention.quote_language:
                quote_info['language'] = intervention.quote_language.name
                quote_info['language code'] = intervention.quote_language.code
            data['quote'] = quote_info

        if intervention.author:
            data['annotator'] = intervention.author.authorized_name

        return data
