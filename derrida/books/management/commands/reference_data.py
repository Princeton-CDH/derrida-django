import codecs
import csv
import json
import os.path

from django.core.management.base import BaseCommand

from derrida.books.models import DerridaWork


class Command(BaseCommand):
    '''Export reference data for each Derrida Work as CSV and JSON'''
    help = __doc__

    #: fields for CSV output
    csv_fields = [
        'page', 'page location', 'type', 'book title', 'book id',
        'book page', 'book type', 'anchor text', 'interventions'
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '-d', '--directory',
            help='Specify the directory where files should be generated')

    def handle(self, *args, **kwargs):

        for derrida_work in DerridaWork.objects.all():
            base_filename = '%s_references' % derrida_work.slug
            if kwargs['directory']:
                base_filename = os.path.join(kwargs['directory'], base_filename)

            # generate filenames based on slug ?
            # Can we use the same data to generate both CSV and JSON?

            # aggregate reference data to be exported for use in generating
            # CSV and JSON output
            refdata = [self.reference_data(ref)
                       for ref in derrida_work.reference_set.all()]

            # list of dictionaries can be output as is for JSON export
            with open('{}.json'.format(base_filename), 'w') as jsonfile:
                json.dump(refdata, jsonfile, indent=2)

            # generate CSV export
            with open('{}.csv'.format(base_filename), 'w') as csvfile:
                # write utf-8 byte order mark at the beginning of the file
                csvfile.write(codecs.BOM_UTF8.decode())

                csvwriter = csv.DictWriter(csvfile, fieldnames=self.csv_fields)
                csvwriter.writeheader()

                for reference in refdata:
                    csvwriter.writerow(self.flatten_dict(reference))

    def reference_data(self, reference):
        '''Generate a dictionary of data to export for a single
         :class:`~derrida.books.models.Reference` object'''
        return {
            'page': reference.derridawork_page,
            'page location': reference.derridawork_pageloc,
            'book': {
                'id': reference.instance.get_uri(),
                'title': reference.instance.display_title(),
                'page': reference.book_page,
                'type': reference.book.item_type,
            },
            'type': str(reference.reference_type),
            'anchor text': reference.anchor_text,
            # use intervention URI as identifier
            'interventions': [
                intervention.get_uri()
                for intervention in reference.interventions.all()
            ]
        }

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
