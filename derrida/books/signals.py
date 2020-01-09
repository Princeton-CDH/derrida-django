import logging

from django.db import models
from haystack.exceptions import NotHandled
from haystack.signals import RealtimeSignalProcessor

from derrida.books.models import Instance, Work, Reference
from derrida.outwork.models import Outwork
from derrida.interventions.models import Intervention


logger = logging.getLogger(__name__)


class RelationSafeRTSP(RealtimeSignalProcessor):

    def handle_save(self, sender, instance, **kwargs):
        """
        This code is entirely adapted from Haystack source with custom handling
        of the Instance model to cascade updates. Using super did not clarify
        code in a useful way.

        Searches gets all backends in use, iterates through them, for all
        models.

        Custom handling makes updates to an Instance also trigger an reindex on
        all of the Reference and Intervention instances associated with it.

        """

        # NOTE: could refine this logic to take advantage of
        # information in kwargs, including created flag and
        # update fields
        # https://docs.djangoproject.com/en/2.0/ref/signals/#post-save

        using_backends = self.connection_router.for_write(instance=instance)
        for using in using_backends:
            uindex = self.connections[using].get_unified_index()
            try:
                logger.debug('Indexing %r' % instance)
                index = uindex.get_index(sender)
                index.update_object(instance, using=using)
            except NotHandled:
                # models without an index configured should be ignored
                pass

            # construct a list of additional items that need
            # to be updated in the index; should be a tuple of
            # model class and queryset
            related_updates = []

            if sender == Work:
                # if sender is Work, we need to check for Instances,
                # References and Interventions and reindex them too.
                related_updates = [
                    # all instances associated with current work
                    (Instance, instance.instance_set.all()),
                    # any reference associated with instances of this work
                    (Reference, Reference.objects.filter(instance__work=instance)),
                    # any intervention associated with pages on a digital
                    # edition for an instance of this work
                    (Intervention, Intervention.objects \
                        .filter(canvas__manifest__instance__work=instance)),
                ]

            elif sender == Instance:
                related_updates = [
                    (Reference, Reference.objects.filter(instance=instance)),
                    (Intervention, Intervention.objects \
                        .filter(canvas__manifest__instance=instance)),
                ]

            # index any related objects based on current change
            if related_updates:
                # this is basically what index.update_object does,
                # except we are skipping the should_update check
                # (which defaults to true anyway)
                for klass, items in related_updates:
                    # if there are any items to index, handle them
                    if items:
                        # NOTE: could use klass._meta.verbose_name.title()
                        # and verbose_name_plural here; class maybe more useful
                        logger.debug('Indexing %d %s%s' % (items.count(), klass.__name__,
                            '' if items.count() == 1 else 's'))
                        index = uindex.get_index(klass)
                        backend = index.get_backend(using)
                        backend.update(index, items)

    def setup(self):
        # default haystack behavior is to listen to all models
        # override and only bind to models we index or that affect indexes
        for model in Work, Instance, Reference, Intervention, Outwork:
            models.signals.post_save.connect(self.handle_save, sender=model)
            # (we probably don't care about delete for Work, but ok to leave...)
            models.signals.post_delete.connect(self.handle_delete, sender=model)

    def teardown(self):
        # default haystack behavior; does this work to clear model-specific
        # senders or does it need to match the connect call?

        # Naive (listen to all model saves).
        models.signals.post_save.disconnect(self.handle_save)
        models.signals.post_delete.disconnect(self.handle_delete)
