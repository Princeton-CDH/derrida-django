import pandas as pd
import re
from collections import defaultdict
from html import unescape

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from derrida.books.models import Book, Catalogue, OwningInstitution, CreatorType
from derrida.places.models import Place
from derrida.places.geonames import GeoNamesAPI
from derrida.people.models import Person
from derrida.people.viaf import ViafAPI


class Command(BaseCommand):
    help = 'Import records from Derrida\'s Margins Zotero'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', help='Path to CSV file in Zotero format')

    def handle(self, *args, **options):
        zotero_import = self.clean_data(options['csvfile'])
        self.stats = defaultdict(int)
        # Build an institution entry for princeton
        princeton, created = Place.objects.get_or_create(
            name='Princeton, NJ',
            **(self.geonames_lookup('Princeton, NJ'))
        )
        OwningInstitution.objects.get_or_create(
            short_name='PUL',
            contact_info='http://library.princeton.edu/help/contact-us',
            place=princeton
        )

        for index, row in zotero_import.iterrows():
            try:
                self.create_book(row)
            except Exception as err:
                print('Error: %s - %s' % (row['Title'], err))


        print('''Import either created or found:
        %(book_count)d books
        %(place_count)d places
        %(person_count)d people
        %(publisher_count)d publishers

        %(error_count)d errors''' % self.stats)

    def clean_data(self, csvfile):
        '''Method to import data and clean up fields'''
        # Import CSV and add initial handling
        zotero_data = pd.read_csv(csvfile)
        # Subset just the columsn we care about
        wanted_columns = [
            'Key',
            'Item Type',
            'Publication Year',
            'Author',
            'Title',
            'Translator',
            'Editor',
            'Url',
            'Publisher',
            'Place',
            'Language',
            'Extra',
            'Notes',
            'Manual Tags',
            ]
        zotero_data = zotero_data[wanted_columns]
        # Set NaNs to None for Py3 falsy compatibility
        zotero_data = zotero_data.fillna('')
        # For now, remove rows that are not 'book' or 'bookSection'
        keep_types = ['book', 'bookSection']
        zotero_data = zotero_data.loc[zotero_data['Item Type'].isin(keep_types)]

        # Handle HTML in comment fields
        def strip_html(text):
            if text:
                remove = re.compile(r'<.*?>')
                return unescape(re.sub(remove, '', text))

        zotero_data['Notes'] = zotero_data['Notes'].apply(strip_html)
        return zotero_data

    def create_book(self, row):
        '''Create a book object and associated models'''
        # Create a dictionary and fill in the stuff that can be dropped in
        newbook_dict = {
            'title': row['Title'],
            'pub_year': 'Publication Year',
            'short_title': ' '.join(row['Title'].split()[0:2]),
            'original_pub_info': '%s %s' % (row['Publisher'], row['Place']),
            'is_extant': False,
            'is_annotated': False,
        }

        # Start a newbook object
        try:
            newbook = Book.objects.get(title=newbook_dict['title'])
        except ObjectDoesNotExist:
            newbook = Book(**newbook_dict)

        # Place
        # Run a geonames search and return a dict to set the place
        if row['Place']:
            place_dict = self.geonames_lookup(row['Place'])
            place, created = Place.objects.get_or_create(
                    name=row['Place'],
                    **place_dict
                )

            newbook.place = place
            self.stats['place_count'] += 1

        # Save so we can add creators
        newbook.save()

        # Creators
        # Check if any exist in the row (using blank string as falsy)
        # If they do, create create their person entry with a VIAF lookup.
        # Also get/create stub types for the four obvious options
        creator_types = ['Author', 'Editor', 'Series Editor', 'Translator']
        for c_type in creator_types:
            CreatorType.objects.get_or_create(name=c_type)

        for c_type in creator_types:
            if c_type in row:
                # Check to see if this is a list that needs splitting on ;
                if re.match(';', row[c_type]):
                    # If yes, create entries for each (stripe edge whitespace)
                    split_creators = row[c_type].split(';')
                    for creator in split_cleators:
                        person, created = Person.objects.get_or_create(
                            authorized_name=creator.strip(),
                            viaf_id=self.viaf_lookup(creator.strip())
                        )
                        newbook.add_creator(person, c_type)
            else:
                person, created = Person.objects.get_or_create(
                    authorized_name=row[c_type],
                    viaf_id=self.viaf_lookup(row[c_type])
                )
                newbook.add_creator(person, c_type)
                self.stats['person_count'] += 1

        # Add catalogue entry for book
        # TODO: Call numbers?
        Catalogue.objects.get_or_create(
            book=newbook,
            is_current=True,
            institution=OwningInstitution.objects.get(short_name='PUL')
        )

        # Declare the book saved
        self.stats['book_count'] += 1

    def geonames_lookup(self, place_name):
        '''Function to wrap a GeoNames lookup and assign info.
        Returns a dict for Place generator or empty dict'''
        geo = GeoNamesAPI()
        # Get the top hit and presume the API guessed correctly
        result = geo.search(place_name, max_rows=1)
        place_dict = {}
        if result:
            place_dict['latitude'] = float(result[0]['lat'])
            place_dict['longitude'] = float(result[0]['lng'])
            place_dict['geonames_id'] = geo.uri_from_id(result[0]['geonameId'])
            return place_dict
        else:
            return {}

    def viaf_lookup(self, name):
        viaf = ViafAPI()
        viafid = None
        results = viaf.suggest(name)
        # Handle no results
        if results:
            # Check for a 'nametype' and make sure it's personal
            if 'nametype' in results[0]:
                if results[0]['nametype'] == 'personal':
                    viafid = viaf.uri_from_id(results[0]['viafid'])
        return viafid
