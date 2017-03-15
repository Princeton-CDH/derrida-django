import pandas as pd
import re
from collections import defaultdict
from html import unescape

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.management.base import BaseCommand, CommandError

from derrida.books.models import Book, Catalogue, OwningInstitution, \
    CreatorType, Publisher, Reference, ReferenceType, DerridaWork
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
        self.dud_code_list = []
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
                self.stats['error_count'] += 1
                print('Error: %s - %s' % (row['Title'], err))

        print('''Import either created or found:
        %(book_count)d books
        %(place_count)d places
        %(person_count)d people
        %(publisher_count)d publishers
        %(reference_count)d references from tags

        %(error_count)d errors''' % self.stats)

        print(
            "In addition, the following tags looked suspicious: %s"
            % self.dud_code_list
        )

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
            'pub_year': row['Publication Year'],
            'short_title': ' '.join(row['Title'].split()[0:2]),
            'original_pub_info': '%s %s' % (row['Publisher'], row['Place']),
            'is_extant': False,
            'is_annotated': False,
        }

        # Handle books with no year set
        try:
            int(newbook_dict['pub_year'])
        except ValueError:
            newbook_dict['pub_year'] = None

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

        # Publisher
        if row['Publisher']:
            publisher, created = Publisher.objects.get_or_create(
                                    name=row['Publisher']
                                )
            newbook.publisher = publisher
            self.stats['publisher_count'] += 1

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
                    for creator in split_creators:
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

        # Set flags for annotated/extant/etc.
        # Parse the derrida tag
        if row['Manual Tags']:
            split_tags = row['Manual Tags'].split(';')
            for tag in split_tags:
                tag = tag.strip()
                if self.parse_ref_tag(tag, newbook, row):
                    self.stats['reference_count'] += 1

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

    def parse_ref_tag(self, tag, newbook, row):
        '''Code logic to parse Derrida team's tags'''

        # Compile the appropriate re's
        work_re = re.compile(r'^\D+')
        # Assuming citation is on a particular page, and the work abbreviation
        # is lower case. If not, needs fixing.
        page_loc_re = re.compile(r'(?<=[a-z])\d+([a-z])|.')
        annotation_type_re = re.compile(r'[A-Z]')
        book_page_seq_re = re.compile(r'(?<=[A-Z]).+?(?=[A-Z])')
        annotation_status_re = re.compile(r'[A-Z]$')

        work = None
        page_loc = None
        book_page_seq = None
        annotation_type = None
        annotation_status = None

        try:
            work = (re.search(work_re, tag)).group(0)
            page_loc = (re.search(page_loc_re, tag)).group(0)
            annotation_type = (re.search(annotation_type_re, tag)).group(0)
            if re.search(book_page_seq_re, tag):
                book_page_seq = (re.search(book_page_seq_re, tag)).group(0)
            if re.search(annotation_status_re, tag):
                annotation_status = (re.search(annotation_status_re, tag)).group(0)
        except AttributeError:
            self.dud_code_list.append(tag)
        derridawork_mapping = {
            'dg': 'De la grammatologie',
        }

        reference_mapping = {
            'Q': 'Quotation',
            'E': 'Epigraph',
            'C': 'Citation',
            'F': 'Footnote',
        }

        # Set the annotation flags
        try:
            if annotation_status == 'Y':
                newbook.is_extant = True
                newbook.is_annotated = True
            if annotation_status == 'N':
                newbook.is_extant = True
        except:
            self.dud_code_list.append(tag)
        newbook.save()

        # Save make a Reference
        try:
            ref, created = Reference.objects.get_or_create(
                    book=newbook,
                    derridawork=DerridaWork.objects.get(
                                    short_title=derridawork_mapping[work]
                                ),
                    derridawork_page=re.sub(r'[a-z]', '', page_loc),
                    derridawork_pageloc=re.sub(r'[^a-zA-Z0-9]', '', page_loc),
                    reference_type=ReferenceType.objects.get(
                                        name=reference_mapping[annotation_type]),
                    book_page=book_page_seq,
                )
        except KeyError:
            self.dud_code_list.append(tag)
