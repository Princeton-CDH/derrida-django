from django.db import models

from derrida.common.models import Named, Notable


class Place(Named, Notable):
    '''Simple model for tracking places and associated with
    people and books.'''

    #: geonames URI
    geonames_id = models.URLField()
    #: latitude
    latitude = models.FloatField()
    #: longitude
    longitude = models.FloatField()
