from haystack.exceptions import NotHandled
from haystack.signals import RealtimeSignalProcessor

from derrida.books.models import Instance, Work, Reference
from derrida.interventions.models import Intervention


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


        using_backends = self.connection_router.for_write(instance=instance)
        for using in using_backends:
            try:
                index = self.connections[using].get_unified_index().\
                    get_index(sender)
                index.update_object(instance, using=using)
            except NotHandled:
                if sender == Work:
                    # if sender is Work, we need to check for Instances,
                    # References and Interventions and reindex them too.
                    instances = instance.instance_set.all()
                    for instance in instances:
                        index = self.connections[using].get_unified_index()\
                            .get_index(Instance)
                        index.update_object(instance, using=using)

                        references = instance.reference_set.all()
                        interventions = Intervention.objects.filter(
                            canvas__manifest__instance=instance
                        )
                        # update references
                        index = self.connections[using].get_unified_index()\
                            .get_index(Reference)
                        for reference in references:
                            index.update_object(reference, using=using)
                        # update interventions
                        index = self.connections[using].get_unified_index().\
                            get_index(Intervention)
                        for intervention in interventions:
                            index.update_object(intervention, using=using)
                if sender == Instance:
                    index = self.connections[using].get_unified_index()\
                        .get_index(Instance)
                    index.update_object(instance, using=using)

                    references = instance.reference_set.all()
                    interventions = Intervention.objects.filter(
                        canvas__manifest__instance=instance
                    )
                    # update references
                    index = self.connections[using].get_unified_index()\
                        .get_index(Reference)
                    for reference in references:
                        index.update_object(reference, using=using)
                    # update interventions
                    index = self.connections[using].get_unified_index().\
                        get_index(Intervention)
                    for intervention in interventions:
                        index.update_object(intervention, using=using)
