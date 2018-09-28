'''
Manage command to export references cited in all Derrida works to a group
Zotero library. Each work is assumed to correspond to a collection in the
Zotero library.

Command assumes that the target Zotero library ID and a Zotero API key are
populated in local_settings.py.
'''
import pprint
from itertools import islice

import progressbar
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import QuerySet
from django.template.defaultfilters import pluralize
from pyzotero import zotero

from derrida.books.models import DerridaWork, Instance


class Command(BaseCommand):
    '''Export all references in all Derrida works to a Zotero library.'''
    help = __doc__
    pp = pprint.PrettyPrinter(indent=4)
    library = None

    def add_arguments(self, parser):
        parser.add_argument(
            '-d', '--delete', choices=['all', 'collections', 'items'],
            default='all', help='Delete all collections, items, or both (default).'
        )
        parser.add_argument(
            '--no-progress', action='store_true',
            help='Don\'t display progress bar to track the status of the export.'
        )

    def handle(self, *args, **kwargs):
        # check for secrets
        if not getattr(settings, 'ZOTERO_API_KEY', None):
            raise CommandError('Zotero API key must be set.')
        if not getattr(settings, 'ZOTERO_LIBRARY_ID', None):
            raise CommandError('Zotero library ID must be set.')
        # initialize the library
        self.library = zotero.Zotero(settings.ZOTERO_LIBRARY_ID, 'group',
                                     settings.ZOTERO_API_KEY)
        # create new collections for any newly added derrida works (no zotero ID)
        self.create_collections(DerridaWork.objects.filter(zotero_id=''))
        # create/update all items cited in a derrida work
        self.create_items(Instance.objects.filter(cited_in__isnull=False))

    def create_collections(self, works: QuerySet):
        '''
        create zotero collections for the provided derrida works and store the
        generated zotero collection id on the work
        '''
        new = works.count()
        if new > 0:
            self.stdout.write('Found {} new Derrida works.'.format(new))
            res = self.library.create_collections([{'name': work.short_title} for work in works])
            # zotero returns a dict with index (as string) as key and collection id as value
            for index, value in res['success'].items():
                works[int(index)].zotero_id = value
                works[int(index)].save()

    def create_items(self, instances: QuerySet):
        '''
        ensure all instances cited in derrida works are represented as items:
        create new items where no zotero id exists and update those that already
        have an id
        '''
        total = instances.count()
        progbar = progressbar.ProgressBar(redirect_stdout=True, max_value=total)
        instances = instances.iterator()
        chunk_size = 50
        chunk = list(islice(instances, chunk_size))
        count = 0
        initial_items = self.library.count_items()
        stats = {
            'created': 0,
            'updated': 0,
            'unchanged': 0,
            'failed': 0,
            'total': total
        }
        while chunk:
            # convert the instances to zotero items
            items = [instance.as_zotero_item(self.library) for instance in chunk]
            # get the last modified version of the library to send as header
            l_m = self.library.last_modified_version()
            # create_items will automatically update the item if 'key' is passed
            res = self.library.create_items(items, last_modified=l_m)
            progbar.update(count)
            stats['updated'] += len(res['success'])
            stats['unchanged'] += len(res['unchanged'])
            stats['failed'] += len(res['failed'])
            count += chunk_size
            # save any generated zotero ids to the items
            for index, value in res['success'].items():
                chunk[int(index)].zotero_id = value
                chunk[int(index)].save()
            chunk = list(islice(instances, chunk_size))
        final_items = self.library.count_items()
        stats['created'] = final_items - initial_items
        summary = '\nProcessed {:,d} instance{} for export.' + \
        '\nCreated {:,d}; updated {:,d}; unchanged {:,d}; failed {:,d}.'
        summary = summary.format(
            stats['total'], pluralize(stats['total']),
            stats['created'], stats['updated'], stats['unchanged'],
            stats['failed'], pluralize(stats['failed'])
        )
        self.stdout.write(summary)
