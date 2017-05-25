# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse
import json

# Common models between projects and associated new types
from derrida.books.models import Publisher


User = get_user_model()


class TestPubAutocomplete(TestCase):

    def setUp(self):
        user = User.objects.create_superuser(
            username='test',
            password='secret',
            email='foo@bar.com'
        )
        pub = Publisher.objects.create(name='Printing',)

    def test_view_behavior(self):
        # No login for anonymous user
        response = self.client.get(reverse('books:publisher-autocomplete'))
        assert response.status_code == 302

        # Get a response as a staff user
        self.client.login(username='test', password='secret')
        response = self.client.get(
            reverse('books:publisher-autocomplete'),
            params={'q': 'Print'}
        )
        assert response.status_code == 200
        data = json.loads(response.content.decode('utf-8'))
        assert 'results' in data
        assert data['results'][0]['text'] == 'Printing'


