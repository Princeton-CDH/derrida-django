from django.db import models
from django.core.exceptions import ValidationError
# abstract models with common fields to be
# used as mix-ins


class Named(models.Model):
    '''Abstract model with a 'name' field; by default, name is used as
    the string display.'''

    #: unique name (required)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Notable(models.Model):
    '''Abstract model with an optional notes text field'''

    #: optional notes
    notes = models.TextField(blank=True)

    class Meta:
        abstract = True

    def has_notes(self):
        '''boolean flag indicating if notes are present, for display
        in admin lists'''
        return bool(self.notes)
    has_notes.boolean = True


class DateRange(models.Model):
    '''Abstract model with optional start and end years, and a
    custom dates property to display the date range nicely.  Includes
    validation that requires end year falls after start year.'''

    #: start year (optional)
    start_year = models.SmallIntegerField(null=True, blank=True)
    #: end year (optional)
    end_year = models.SmallIntegerField(null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def dates(self):
        '''Date or date range as a string for display'''

        # if no dates are set, return an empty string
        if not self.start_year and not self.end_year:
            return ''

        # if start and end year are the same just return one year
        if self.start_year == self.end_year:
            return self.start_year

        date_parts = [self.start_year, '-', self.end_year]
        return ''.join([str(dp) for dp in date_parts if dp is not None])

    def clean_fields(self, exclude=None):
        '''Override to clean fields to make sure start/end year are sensical'''
        if exclude is None:
            exclude = []
        if 'start_year' in exclude or 'end_year' in exclude:
            return
        # require end year to be greater than or equal to start year
        # (allowing equal to support single-year ranges)
        if self.start_year and self.end_year and \
                not self.end_year >= self.start_year:
            raise ValidationError('End year must be after start year')
