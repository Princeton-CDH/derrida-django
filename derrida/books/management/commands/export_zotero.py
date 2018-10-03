'''
Manage command to export references cited in all Derrida works to a group
Zotero library. Each work is assumed to correspond to a collection in the
Zotero library.

Command assumes that the target Zotero library ID and a Zotero API key are
populated in local_settings.py.
'''
from collections import defaultdict
from itertools import islice

import progressbar
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import QuerySet
from pyzotero import zotero

from derrida.books.models import DerridaWork, Instance


class Command(BaseCommand):
    '''Export all references in all Derrida works to a Zotero library.'''
    help = __doc__
    library = None

    #: normal verbosity level
    v_normal = 1
    #: output verbosity
    verbosity = v_normal

    #: number of items to send to Zotero API per request; Zotero only allows 50
    chunk_size = 50

    # NOTE: options to validate (using pyzotero check_items) and run in
    # no-act mode might be useful

    def handle(self, *args, **kwargs):
        # check for secrets
        if not getattr(settings, 'ZOTERO_API_KEY', None):
            raise CommandError('Zotero API key must be set.')
        if not getattr(settings, 'ZOTERO_LIBRARY_ID', None):
            raise CommandError('Zotero library ID must be set.')

        self.verbosity = kwargs.get('verbosity', self.v_normal)

        # initialize the library
        self.library = zotero.Zotero(settings.ZOTERO_LIBRARY_ID, 'group',
                                     settings.ZOTERO_API_KEY)
        # create new collections for any derrida works with a zotero id
        self.create_collections(DerridaWork.objects.filter(zotero_id=''))
        # create/update all items cited in a derrida work
        stats = self.create_items(Instance.objects.filter(cited_in__isnull=False))
        summary = '\nExport complete. \n\
Created {created:,d}; updated {updated:,d}; unchanged {unchanged:,d}; failed {failed:,d}.'.format(**stats)
        self.stdout.write(summary)

    def create_collections(self, works: QuerySet):
        '''
        create zotero collections for the provided derrida works and store the
        generated zotero collection id on the work
        '''
        new = works.count()
        if new > 0:
            self.stdout.write('Found {} new Derrida work{}.'.format(
                new, '' if new == 1 else 's'))
            res = self.library.create_collections([{'name': work.short_title} for work in works])
            # zotero returns a dict with index (as string) as key and collection id as value
            for index, value in res['success'].items():
                works[int(index)].zotero_id = value
                works[int(index)].save()
        else:
            if self.verbosity > self.v_normal:
                self.stdout.write('No collections to create.')

    def create_items(self, instances: QuerySet):
        '''
        ensure all instances cited in derrida works are represented as items:
        create new items where no zotero id exists and update those that already
        have an id
        '''
        total = instances.count()
        stats = defaultdict(int)

        # nothing to do; bail out
        if not total:
            if self.verbosity > self.v_normal:
                self.stdout.write('No items to create.')
            return

        self.stdout.write('Exporting {} instances.'.format(total))
        progbar = progressbar.ProgressBar(redirect_stdout=True, max_value=total)
        instances = instances.iterator()

        # store initial count to determine how many are added
        initial_count = self.library.count_items()
        count = 0

        # iterate over the queryset in chunks, since Zotero API
        # only allows sending in sets of 50
        chunk = list(islice(instances, self.chunk_size))

        while chunk:
            # using create items with existing zotero id to update requires a
            # last modified; get last modified version of the library.
            # NOTE: must be done for each chunk
            last_mod = self.library.last_modified_version()

            # convert the instances to zotero items
            items = [instance.as_zotero_item(self.library) for instance in chunk]
            res = self.library.create_items(items, last_modified=last_mod)
            progbar.update(count)
            stats['updated'] += len(res['success'])
            stats['unchanged'] += len(res['unchanged'])
            stats['failed'] += len(res['failed'])

            # report any failures
            if res['failed']:
                for index, error in res['failed'].items():
                    self.stderr.write('\nError on %s: %s' % \
                        (chunk[int(index)], error['message']))

            count += self.chunk_size

            # save newly generated zotero ids to the items in the database
            for index, value in res['success'].items():
                chunk[int(index)].zotero_id = value
                chunk[int(index)].save()

            # get the next chunk of items
            chunk = list(islice(instances, self.chunk_size))

        progbar.finish()

        # Determine number of items newly created based on library count.
        stats['created'] = self.library.count_items() - initial_count
        # TODO: success includes created; subtract created from updated?
        return stats
