# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from djiffy.models import Manifest
import json

from derrida.books.models import Publisher, Instance
from derrida.interventions.models import Intervention, INTERVENTION_TYPES


class TestBookViews(TestCase):
    fixtures = ['sample_work_data.json', 'test_canvas_data.json']

    def setUp(self):
        # create an admin user to test autocomplete views
        self.password = 'pass!@#$'
        self.admin = get_user_model().objects.create_superuser('testadmin',
            'test@example.com', self.password)

    def test_publisher_autocomplete(self):
        # Not accessible to anonymous user
        pub_autocomplete_url = reverse('books:publisher-autocomplete')
        response = self.client.get(pub_autocomplete_url)
        assert response.status_code == 302

        # Get a response as a staff user
        self.client.login(username=self.admin.username, password=self.password)
        response = self.client.get(pub_autocomplete_url, params={'q': 'Bacon'})
        assert response.status_code == 200
        data = json.loads(response.content.decode('utf-8'))
        assert 'results' in data
        assert data['results'][0]['text'] == 'Baconnière'

    def test_language_autocomplete(self):
        # Not accessible to anonymous user
        lang_autocomplete_url = reverse('books:language-autocomplete')
        response = self.client.get(lang_autocomplete_url)
        assert response.status_code == 302

        # Get a response as a staff user
        self.client.login(username=self.admin.username, password=self.password)
        response = self.client.get(lang_autocomplete_url, params={'q': 'eng'})
        assert response.status_code == 200
        data = json.loads(response.content.decode('utf-8'))
        assert 'results' in data
        assert data['results'][0]['text'] == 'English'

    def test_instance_admin_editform(self):
        self.client.login(username=self.admin.username, password=self.password)
        inst = Instance.objects.first()
        instance_edit_url = reverse('admin:books_instance_change',
            args=[inst.id])
        response = self.client.get(instance_edit_url)
        # with no interventions, just test that the view renders
        assert response.status_code == 200

        # associate library instance with a digital edition
        manif = Manifest.objects.first()
        inst.digital_edition = manif
        inst.save()
        cnvs1, cnvs2 = manif.canvases.first(), manif.canvases.last()
        # add test interventions to canvases associated with the manifest
        ivtns = Intervention.objects.bulk_create([
            # annotation on canvas 1, no text
            Intervention(uri=cnvs1.uri, canvas=cnvs1,
                intervention_type=INTERVENTION_TYPES.ANNOTATION),
            # annotation on canvas 2 with text
            Intervention(uri=cnvs2.uri, canvas=cnvs2,
                intervention_type=INTERVENTION_TYPES.ANNOTATION,
                text='Some annotation comment here'),
            # insertion on canvas 2 with text
            Intervention(uri=cnvs2, canvas=cnvs2,
                intervention_type=INTERVENTION_TYPES.INSERTION,
                text='A different insertion comment here'),
        ])
        response = self.client.get(instance_edit_url)
        self.assertTemplateUsed(template_name='admin/books/instance/change_form.html')

        self.assertContains(response, cnvs1.label, count=1,
            msg_prefix='canvas label should appear once for each associated intervention')
        self.assertContains(response, cnvs2.label, count=2,
            msg_prefix='canvas label should appear once for each associated intervention')
        self.assertContains(response, cnvs1.get_absolute_url(), count=1,
            msg_prefix='canvas url should be included once for each associated intervention')
        self.assertContains(response, cnvs2.get_absolute_url(), count=2,
            msg_prefix='canvas url should be included once for each associated intervention')
        self.assertContains(response, 'Annotation', count=2,
            msg_prefix='intervention type should display for each item')
        self.assertContains(response, 'Intervention', count=3,
            msg_prefix='intervention type should display for each item, once in'
            ' the reference inline, and once in the hidden reference inline')

        for intervention in ivtns:
            self.assertContains(response, intervention.admin_thumbnail(),
                msg_prefix='should display admin thumbnail for each intervention')
            self.assertContains(response, intervention.text_preview(),
                msg_prefix='should display text preview for each intervention')
            self.assertContains(response,
                reverse('admin:interventions_intervention_change', args=[intervention.id]),
                msg_prefix='should link to intervention edit page')
