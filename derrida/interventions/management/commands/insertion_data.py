'''
Manage command to export intervention insertions data for use by others.

Generates a CSV and JSON file with details for all insertions
documented via IIIF canvas image labels in the database.

Takes an optional argument to specify the output directory. Otherwise,
files are created in the current directory.
'''


import codecs
from collections import OrderedDict, defaultdict
import csv
import json
import os.path
import re
from itertools import groupby

from django.db.models import ObjectDoesNotExist
from djiffy.models import Canvas

from derrida.interventions.management.commands import annotation_data
from derrida.interventions.models import Intervention


# regex to extract insertion label common to all images
# for a single insertion from the canvas label
# grouping for full label, page range/label in book, insertion page label
RE_INSERTION_LABEL = re.compile(r'(?P<label>(?P<page>.*)Insertions? [A-Z])(?P<insertion_page>.*$)')


class Command(annotation_data.Command):
    '''Export intervention insertion data from the database as CSV and JSON'''
    help = __doc__

    # NOTE: extending annotation_data manage command to inherit
    # flatten_data method & localize_iiif_image

    #: fields for CSV output
    csv_fields = [
        # match annotation fields where possible (but not a lot of overlap)
        'id',
        'book_id', 'book_title', 'book_type', 'page',
        'num_images', 'image_labels', 'image_iiif'
    ]

    #: base filename, for CSV and JSON output
    base_filename = 'insertions'

    def handle(self, *args, **kwargs):
        if kwargs['directory']:
            self.base_filename = os.path.join(kwargs['directory'], self.base_filename)

        # aggregate intervention data to be exported for use in generating
        # CSV and JSON output

        # canvas label indicates if a canvas is part of an insertion
        insertion_canvases = Canvas.objects.filter(label__contains='Insertion')

        insertion_images = defaultdict(list)
        for canvas in insertion_canvases:
            insertion_match = RE_INSERTION_LABEL.match(canvas.label)
            if not insertion_match:
                print('ERROR: regex fails on %s' % canvas.label)
                continue

            # construct group label from manifest label and insertion title within canvas label
            # so we get unique image groups for each logical insertion
            group_label = '%s. %s' % (canvas.manifest.label.strip('.'), insertion_match.group('label'))
            insertion_images[group_label].append(canvas)

        data = [self.insertion_data(label, canvas_group)
                for label, canvas_group in insertion_images.items()]

        # filter out any null values for canvases not linked to work instance
        data = [d for d in data if d]

        # list of dictionaries can be output as is for JSON export
        with open('{}.json'.format(self.base_filename), 'w') as jsonfile:
            json.dump(data, jsonfile, indent=2)

        # generate CSV export
        with open('{}.csv'.format(self.base_filename), 'w') as csvfile:
            # write utf-8 byte order mark at the beginning of the file
            csvfile.write(codecs.BOM_UTF8.decode())

            csvwriter = csv.DictWriter(csvfile, fieldnames=self.csv_fields)
            csvwriter.writeheader()

            for insertion in data:
                csvwriter.writerow(self.flatten_dict(insertion))

    def insertion_data(self, label, canvases):
        '''Generate a dictionary of data to export for a group
        of canvases representing a single insertion in a single book.'''

        # NOTE: using OrderedDict to ensure JSON output follows logical
        # order in Python < 3.6, where dict order is not guaranteed

        first_canvas = canvases[0]
        # access book via manifest instance (reverse of digital edition relation)
        # at least one insertion canvas is not related to a book...
        try:
            book = first_canvas.manifest.instance
        except ObjectDoesNotExist:
            print('manifest %s not related to work instance' % first_canvas.manifest.label)
            # NOTE: one manifest is not linked, and it seems to be a duplicate;
            # omit from export
            book = None
            return

        # extract page number from first canvas label
        page = RE_INSERTION_LABEL.match(first_canvas.label).group('page')

        return OrderedDict([
            ('id', label),   # provisional
            ('book', OrderedDict([
                ('id', book.get_uri()),
                ('title', book.display_title()),
                ('type', book.item_type)
            ])),
            # some page labels include "with";
            # not easy to ignore out via regex, so just remove here
            ('page', page.replace(" with", "").strip()),
            ('num_images', len(canvases)),
            # to avoid repetition, only include unique portion of the label
            # (i.e., recto/verso or roman numerals for multipage items)
            ('image_labels', [RE_INSERTION_LABEL.match(c.label).group('insertion_page').strip()
                              for c in canvases]),
            ('image_iiif', [
                # use local version of iiif image; limit width to 500
                str(self.localize_iiif_image(c, book).size(width=500)) for c in canvases
            ])
        ])
