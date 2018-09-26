'''
Manage command to export references cited in all Derrida works to a group
Zotero library. Each work is assumed to correspond to a collection in the
Zotero library.

Command assumes that the target Zotero library ID and a Zotero API key are
populated in local_settings.py.
'''
import pprint
from itertools import islice

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from pyzotero import zotero

from derrida.books.models import DerridaWork, Instance


class Command(BaseCommand):
    '''Export all references in all Derrida works to a Zotero library.'''
    help = __doc__

    def handle(self, *args, **kwargs):
        # check for necessary settings
        if not getattr(settings, 'ZOTERO_API_KEY', None):
            raise CommandError('Zotero API key must be set.')
        if not getattr(settings, 'ZOTERO_LIBRARY_ID', None):
            raise CommandError('Zotero library ID must be set.')
        # retrieve the library and some item type templates
        library = zotero.Zotero(settings.ZOTERO_LIBRARY_ID, 'group',
                                settings.ZOTERO_API_KEY)
        pp = pprint.PrettyPrinter(indent=4)
        # ensure all derrida works are represented as collections:
        # create zotero collections for any derrida work without a zotero id;
        # store that collection's zotero id on the work
        new_collections = DerridaWork.objects.filter(zotero_id='')
        created = library.create_collections([{'name': work.short_title} for work in new_collections])
        # zotero returns a dict with index (as string) as key and collection id as value
        for index, value in created['success'].items():
            new_collections[int(index)].zotero_id = value
            new_collections[int(index)].save()
        # create items
        instances = Instance.objects.filter(cited_in__isnull=False).iterator()
        chunk_size = 10
        chunk = list(islice(instances, chunk_size))
        count = 0
        while chunk:
            # convert the instances to zotero items
            items = [instance.as_zotero_item(library) for instance in chunk]
            # add a last-modified timestamp for use with if-modified-since header
            # timestamps = []
            # create_items will automatically update the item if 'key' is passed
            created = library.create_items(items)
            print(created)
            # save any generated zotero ids to the item
            for index, value in created['success'].items():
                chunk[int(index)].zotero_id = value
                chunk[int(index)].save()
            chunk = list(islice(instances, chunk_size))

        # for item in library.items():
        #     library.delete_item(item)

        # for collection in library.collections():
        #     library.delete_collection(collection)
