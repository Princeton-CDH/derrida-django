from django.test import TestCase

# Create your tests here.

class TargetTest(TestCase):
    '''Dummy test case for Travis-CI integration'''
    def test_is_zero_zero(self):
        assert 0 == 0
