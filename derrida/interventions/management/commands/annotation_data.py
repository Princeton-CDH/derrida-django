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

from django.urls import reverse

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
        'id', 'book_id', 'book_title', 'book_type', 'page', 'tags', 'text_content',
        'text_language', 'text_language_code', 'text_translation',
        'quote_content', 'quote_language', 'quote_language_code', 'annotator',
        'annotation_region', 'ink', 'page_iiif',
    ]

    #: base filename, for CSV and JSON output
    base_filename = 'annotations'

    def handle(self, *args, **kwargs):
        if kwargs['directory']:
            self.base_filename = os.path.join(kwargs['directory'], self.base_filename)

        # aggregate intervention data to be exported for use in generating
        # CSV and JSON output
        data = [self.annotation_data(intervention)
                   for intervention in Intervention.objects.all()]

        # list of dictionaries can be output as is for JSON export
        with open('{}.json'.format(self.base_filename), 'w') as jsonfile:
            json_data = self.remove_empty_keys(data)
            json.dump(json_data, jsonfile, indent=2)

        # generate CSV export
        with open('{}.csv'.format(self.base_filename), 'w') as csvfile:
            # write utf-8 byte order mark at the beginning of the file
            csvfile.write(codecs.BOM_UTF8.decode())

            csvwriter = csv.DictWriter(csvfile, fieldnames=self.csv_fields)
            csvwriter.writeheader()

            for intervention in data:
                csvwriter.writerow(self.flatten_dict(intervention))

    def annotation_data(self, intervention):
        '''Generate a dictionary of data to export for a single
        :class:`~derrida.books.models.Reference` object'''

        # NOTE: using OrderedDict to ensure JSON output follows logical
        # order in Python < 3.6, where dict order is not guaranteed

        if intervention.canvas:
            canvas_url = reverse('books:canvas-image', kwargs={
                'slug': intervention.work_instance.slug,
                'short_id': intervention.canvas.short_id, 
                'mode': 'large',
            })
            page_iiif = 'https://derridas-margins.princeton.edu' + canvas_url
            page_iiif = page_iiif.replace('/large/', '/iiif/full/500,/0/default.jpg')
        else:
            page_iiif = ''

        # annotation_region = #

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
            ('ink', intervention.ink),
            ('page_iiif', page_iiif),
            ('annotation_region', str(intervention.iiif_image_selection())),
        ])

        # only include text and quote information if we have content
        if intervention.text:
            text_info = OrderedDict({
                'content': intervention.text
            })
            if intervention.text_language:
                text_info['language'] = intervention.text_language.name
                text_info['language_code'] = intervention.text_language.code
            if intervention.text_translation:
                text_info['translation'] = intervention.text_translation

            data['text'] = text_info

        if intervention.quote:
            quote_info = OrderedDict({
                'content': intervention.quote
            })
            if intervention.quote_language:
                quote_info['language'] = intervention.quote_language.name
                quote_info['language_code'] = intervention.quote_language.code
            data['quote'] = quote_info

        if intervention.author:
            data['annotator'] = intervention.author.authorized_name

        return data
