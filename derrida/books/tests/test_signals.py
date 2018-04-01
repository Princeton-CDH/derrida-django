from unittest import mock

from django.db.models import QuerySet
from django.test import TestCase
from haystack.exceptions import NotHandled

from derrida.books.models import Work, Instance, Reference
from derrida.books.signals import RelationSafeRTSP
from derrida.interventions.models import Intervention


class TestRelationSafeRTSP(TestCase):
    fixtures = ['test_references.json']

    def test_handle_save(self):
        mock_connection = mock.Mock()
        mock_connections = {'default': mock_connection}
        mock_connection_router = mock.Mock()
        mock_connection_router.for_write.return_value = ['default']
        mock_connection.get_unified_index.return_value.get_index.side_effect = NotHandled

        # NOTE: initiializing the signal processor connects
        # the post_save signal handlers
        relsafe = RelationSafeRTSP(mock_connections, mock_connection_router)
        # NOTE: could init with haystack connections & router
        # but that makes it much harder to test what is going on
        # import haystack
        # relsafe = RelationSafeRTSP(haystack.connections, haystack.connection_router)

        # signal setup means the save handler automatically runs on object create
        wk = Work.objects.create(short_title='Foo')
        # work is not indexed, should raise not handled
        # work with no related objects - should not error
        mock_connection_router.for_write.assert_called_with(instance=wk)
        mock_connection.get_unified_index.assert_called_with()
        mock_connection.get_unified_index.return_value.get_index.assert_called_with(Work)
        search_index = mock_connection.get_unified_index.return_value.get_index.return_value
        search_index.update_object.assert_not_called()

        # load instance with multiple references from reference fixture
        inst = Instance.objects.get(pk=2)
        # save the work this instance is associated with
        mock_connection.reset()
        # raise not handled on first get index call (for Work), default behavior for rest
        mock_connection.get_unified_index.return_value.get_index.side_effect = [
            NotHandled, mock.DEFAULT, mock.DEFAULT, mock.DEFAULT]
        # when the work is saved, instance should be reindexed
        relsafe.handle_save(Work, inst.work)
        mock_connection.get_unified_index.return_value.get_index.assert_any_call(Instance)
        mock_connection.get_unified_index.return_value.get_index.assert_any_call(Reference)
        search_index.get_backend.assert_called_with('default')

        # second to last call is instance update
        instance_update_call = search_index.get_backend.return_value.update.call_args_list[-2]
        instance_update_call_args = instance_update_call[0]
        assert instance_update_call_args[0] == search_index
        # NOTE: django has an assertQuerysetEqual test, but it fails here for some reason
        # (needs list of values? but list format also fails)
        # self.assertQuerysetEqual(instance_update_call_args[1], wk.instance_set.all())
        assert isinstance(instance_update_call_args[1], QuerySet)
        assert instance_update_call_args[1].count() == 1
        assert instance_update_call_args[1].first() == inst

        # last call is reference update
        ref_update_call = search_index.get_backend.return_value.update.call_args
        ref_update_call_args = ref_update_call[0]
        assert ref_update_call_args[0] == search_index
        assert isinstance(ref_update_call_args[1], QuerySet)
        assert ref_update_call_args[1].count() == inst.reference_set.count()
        assert ref_update_call_args[1].first() == inst.reference_set.first()



