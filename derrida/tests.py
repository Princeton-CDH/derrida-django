'''Tests for utility functions for Derrida'''
from derrida.utils import deligature


def test_deligature():
    '''Check that deligature removes unicode Latin ligatures'''
    ligatured = 'Œ œ Æ æ'
    assert deligature(ligatured) == 'Oe oe Ae ae'
