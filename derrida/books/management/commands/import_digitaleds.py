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
from collections import defaultdict

from django.core.management.base import BaseCommand
from djiffy.importer import ManifestImporter

from derrida.books.models import Instance


class DerridaManifestImporter(ManifestImporter):
    '''Extends :class:`djiffy.importer.ManifestImporter` to add additional
    logic for associating the imported :class:`djiffy.models.Manifest`
    with an existing :class:`winthrop.books.models.Book`'''

    stats = defaultdict(int)

    def import_manifest(self, manifest, path):
        # parent method returns newly created db manifest
        # or None if there was an error or manifest was already imported
        self.stats['urls'] += 1
        db_manifest = super(DerridaManifestImporter, self) \
            .import_manifest(manifest, path)
        if not db_manifest:
            return

        short_id = db_manifest.short_id
        self.stats['manifests'] += 1

        self.output('Imported %s "%s"' % (short_id, db_manifest.label))

        # Attempt to find the corresponding Derrida library instance object
        # for this digital edition and associate them.
        # - manifests from plum include a url identifier as a "seeAlso"
        # link; for archival items, this is the finding aid url.
        findingaid_url = None
        for url in db_manifest.extra_data.keys():
            if 'findingaids.princeton.edu' in url:
                findingaid_url = url
                break

        # if a finding aid url was found, clean it up for matching
        # against the finding aid urls in project data
        if findingaid_url:
            # remove https since local urls use http
            findingaid_url = findingaid_url.replace('https://', '')
            # remove trailing .xml?scope=record for matching purposes
            findingaid_url = findingaid_url.split('.xml')[0]

            items = Instance.objects.filter(uri__contains=findingaid_url)
            # only associate if one and only one match is found
            if items.count() == 1:
                instance = items.first()
                instance.digital_edition = db_manifest
                instance.save()
                self.output('  Associated %s with "%s"' % (short_id, instance))
            elif items.count() > 1:
                self.error_msg('  Found %d matching instances for %s' % \
                    (items.count(), findingaid_url))
                self.stats['nomatch'] += 1
            else:
                self.error_msg('No matching instance for %s (%s)' % \
                    (short_id, findingaid_url))
                self.stats['nomatch'] += 1

        else:
            self.error_msg('No finding aid URL found for %s' % short_id)

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
        dmi = DerridaManifestImporter(stdout=self.stdout, stderr=self.stderr,
                                     style=self.style)
        dmi.import_paths(manifest_paths)
        self.summarize(dmi.stats)

    def summarize(self, stats):
        # briefly summarize what was done
        self.stdout.write('\nURLs processed: %(urls)d' % stats)
        if stats['manifests']:
            self.stdout.write('Manifests imported: %(manifests)d' % stats)
            if stats['nomatch']:
                self.stdout.write('Manifests not matched to library work instances: %(nomatch)d' \
                    % stats)


