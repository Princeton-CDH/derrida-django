'''
Manage command to import digitized book content viaf IIIF.  It takes
both files and URLs, and supports both IIIF Collections and single
Manifests.  If a collection is specified, all supported manifests in the
system will be loaded.  If a manifest is already loaded, it will be
skipped (updating manifests is not yet supported).  For convenience, you
use the preset path "PUL" to load the Princeton University Libraries
collection of Derrida materials.

Example use::

    python manage.py import_digitaleds https://plum.princeton.edu/collections/p4j03fz143/manifest
    python manage.py import_digitaleds https://plum.princeton.edu/concern/scanned_resources/pb2775t87z/manifest
    python manage.py import_digitaleds manifest1.json manifest2.json
    python manage.py import_digitaleds PUL

When a local identifier is present in manifest metadata, it will be used
to link the cached manifest in the django database with the appropriate
:class:`winthrop.books.models.Book`.
'''

from django.core.management.base import BaseCommand
from djiffy.importer import ManifestImporter

from derrida.books.models import Instance


class DerridaManifestImporter(ManifestImporter):
    '''Extends :class:`djiffy.importer.ManifestImporter` to add additional
    logic for associating the imported :class:`djiffy.models.Manifest`
    with an existing :class:`winthrop.books.models.Book`'''

    def import_manifest(self, manifest, path):
        # parent method returns newly created db manifest
        # or None if there was an error or manifest was already imported
        db_manifest = super(DerridaManifestImporter, self) \
            .import_manifest(manifest, path)
        if not db_manifest:
            return

        # **NOTE** source metadata identifier implementation is provisional,
        # since that field is not yet included in the manifest seeAlso data

        # Attempt to find the corresponding Derrida library instance object
        # for this digital edition and associate them.
        # - manifests from plum include a source metadata identifier
        #   that looks like RBD1.1_c478
        #   Use that to find instances in the local database by
        #   finding aid url, which looks like:
        #   http://findingaids.princeton.edu/collections/RBD1/c9157
        if 'Source metadata identifier' in db_manifest.metadata:
            source_id = db_manifest.metadata['Source metadata identifier'][0]
            fa_collection, item_id = source_id.split('.')
            findingaid_url = 'http://findingaids.princeton.edu/collections/%s/%s' % \
                (fa_collection, item_id)
            items = Instance.objects.filter(uri=findingaid_url)
            # only associate if one and only one match is found
            if items.count() == 1:
                instance = items.first()
                instance.digital_edition = db_manifest
                instance.save()

            else:
                self.error_msg('No matching instance for %s' % source_id)

        else:
            self.error_msg('No source metadata identifier found')

        return db_manifest


class Command(BaseCommand):
    '''Import digital editions and associate with Winthrop books'''
    help = __doc__

    # shorthand for known URIs to be imported
    manifest_uris = {
        'PUL': 'https://plum.princeton.edu/collections/pb5646r538/manifest'
    }

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+',
            help='''One or more IIIF Collections or Manifests as file or URL.
            Use 'PUL' to import PUL Derrida materials.''')

    def handle(self, *args, **kwargs):
        # convert any shorthand ids into the appropriate manifest uri
        manifest_paths = [self.manifest_uris[p] if p in self.manifest_uris else p
                          for p in kwargs['path']]
        DerridaManifestImporter(stdout=self.stdout, stderr=self.stderr,
                                 style=self.style) \
            .import_paths(manifest_paths)


