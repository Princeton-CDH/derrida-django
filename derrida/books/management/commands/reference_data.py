import codecs
import csv
import json

from django.core.management.base import BaseCommand

from derrida.books.models import DerridaWork


class Command(BaseCommand):
    '''Export reference data'''
    help = __doc__

    def handle(self, *args, **kwargs):

        for derrida_work in DerridaWork.objects.all():
            filename = '%s_references.csv' % derrida_work.slug
            # generate filenames based on slug ?
            # Can we use the same data to generate both CSV and JSON?

            with open(filename, 'w') as csvfile:
                # write utf-8 byte order mark at the beginning of the file
                csvfile.write(codecs.BOM_UTF8.decode())

                fieldnames = [
                    'page', 'page location', 'book title', 'book id',
                    'book page', 'reference type',
                    'anchor text', 'corresponding interventions'
                ]
                csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
                csvwriter.writeheader()

                for reference in derrida_work.reference_set.all():
                    csvwriter.writerow({
                        'page': reference.derridawork_page,
                        'page location': reference.derridawork_pageloc,
                        'book title': reference.instance.display_title(),
                        'book id': reference.instance.id, ## provisional; needs URI
                        'book page': reference.book_page,
                        'reference type': reference.reference_type,
                        'anchor text': reference.anchor_text,
                        # use intervention URI as identifier
                        'corresponding interventions': '; '.join([
                            intervention.get_uri()
                            for intervention in reference.interventions.all()])
                    })
