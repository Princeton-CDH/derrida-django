from unittest.mock import Mock

from django.test import TestCase

from derrida.books.models import Work, Instance, Reference
from derrida.books.signals import RelationSafeRTSP


class TestRelationSafeRTSP(TestCase):

    def test_handle_save(self):
        mock_backend = Mock()
        mock_connections = {'default': mock_backend}
        mock_connection_router = Mock()
        mock_connection_router.for_write.return_value = ['default']
        relsafe = RelationSafeRTSP(mock_connections, mock_connection_router)

        wk = Work.objects.create(short_title='Foo')
        # work with no related objects - should not error
        relsafe.handle_save(Work, wk)
        mock_connection_router.for_write.assert_called_with(instance=wk)
        mock_backend.get_unified_index.assert_called_with()
        mock_backend.get_unified_index.return_value.get_index.assert_called_with(Work)
        search_index = mock_backend.get_unified_index.return_value.get_index.return_value
        search_index.update_object.assert_called_with(wk, using='default')

        # work with instance
        inst = Instance.objects.create(work=wk)
        relsafe.handle_save(Instance, inst)
        mock_backend.get_unified_index.return_value.get_index.assert_called_with(Instance)
        search_index.update_object.assert_called_with(inst, using='default')
