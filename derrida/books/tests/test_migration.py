# -*- coding: utf-8 -*-
import os

from django.core.management import call_command
import pytest

from derrida.people.models import Person
# Common models between projects and associated new types
from derrida.books.models import Book, Work, Instance, CreatorType, ItemType
# Citationality extensions
# from derrida.books.models import DerridaWork, DerridaWorkBook, Reference, ReferenceType, \
    # Work
# data migration from book to work
from derrida.books import migration_utils


FIXTURE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    '..', 'fixtures')

# migration utilities for splitting books out into works/instances

def test_cleaned_title():
    assert migration_utils.cleaned_title('foo') == 'foo'
    assert migration_utils.cleaned_title('essais (manuscrit)') == 'essais'
    assert migration_utils.cleaned_title('Emile [some edition]') == 'Emile'
    assert migration_utils.cleaned_title("Émile ou de l'éducation") == \
        "Emile ou de l'education"


def test_parse_page_range():
    assert migration_utils.parse_page_range('3-4') == ['3', '4']
    assert migration_utils.parse_page_range('123-456') == ['123', '456']
    assert migration_utils.parse_page_range('I-LII') == ['I', 'LII']
    assert migration_utils.parse_page_range('123') == ['123', '123']

    with pytest.raises(Exception):
        migration_utils.parse_page_range('Jan-32')


@pytest.mark.django_db
def test_belongs_to_work():
    # create book and work to test comparison
    author = Person.objects.create(authorized_name='An Author')
    author2 = Person.objects.create(authorized_name='Another Author')
    item_type = ItemType.objects.all().first()
    CreatorType.objects.create(name='Author')
    book = Book.objects.create(primary_title='Essais',
        item_type=item_type)

    work = Work.objects.create(primary_title='Essais')

    # matching titles, no authors
    assert migration_utils.belongs_to_work(book, work)
    # case difference in titles
    book.primary_title = 'essais'
    assert migration_utils.belongs_to_work(book, work)
    # extra content in title
    book.primary_title = 'Essais (manuscrit)'
    assert migration_utils.belongs_to_work(book, work)
    book.primary_title = 'Essais [later edition]'
    assert migration_utils.belongs_to_work(book, work)

    # author mismatch
    work.authors.add(author)
    assert not migration_utils.belongs_to_work(book, work)
    # one author matches
    book.add_author(author)
    assert migration_utils.belongs_to_work(book, work)
    # author work has more authors
    work.authors.add(author2)
    assert not migration_utils.belongs_to_work(book, work)
    book.add_author(author2)
    # author match with two authors
    assert migration_utils.belongs_to_work(book, work)

@pytest.mark.django_db
def test_data_migration():
    book_data = os.path.join(FIXTURE_DIR, 'test_book_migration.json')

    # migrate to *before* books/work data migration
    call_command('migrate', 'books', '0030', verbosity=1)
    # load book fixture data
    call_command('loaddata', book_data, verbosity=2)
    call_command('migrate', 'books', '0031', verbosity=1)
    # run books to works data migration

    # inspect the works/instances generated from fixture book data

    ### Test Case 1
    # Plato / Phedre.  Test data includes three copies of the Phaedrus
    # (`Phèdre`); two are part of complete works and one is in a
    # publication of the Symposion (`Le Banquet`).  Expected outcome:
    # 1) three works: Phèdre, Le Banquet, Œuvres complètes
    # 2) three instances of `Phèdre`, one instance of the `Le Banquet`
    #    and one `Œuvres complètes`
    # 3) Two instances of `Phedre` associated with `Œuvres complètes`
    #    and one with `Le Banquet`

    # migration should generate three works: Phèdre, Le Banquet, Œuvres complètes
    plato_works = Work.objects.filter(authors__authorized_name='Platon')
    assert plato_works.count() == 3
    work_titles = [work.primary_title for work in plato_works]
    for title in ['Phèdre', 'Le Banquet / Phèdre', 'Œuvres complètes']:
        assert title in work_titles
    # migration should generate 5 instances (3 copies of Phèdre, two collections)
    plato_instances = Instance.objects.filter(work__authors__authorized_name='Platon')
    assert plato_instances.count() == 5
    # two instances of Phedre
    assert plato_instances.filter(work__primary_title='Phèdre').count() == 3
    # inspect book sections / collected works
    banquet = plato_instances.get(work__primary_title='Le Banquet / Phèdre')
    assert banquet.work.year == 1964
    assert 'Stub collection instance' in banquet.notes
    assert banquet.collected_set.count() == 1

    oevres = plato_instances.get(work__primary_title='Œuvres complètes')
    assert oevres.work.year == 1938
    assert 'Stub collection instance' in oevres.notes
    assert oevres.collected_set.count() == 2
    assert oevres.collected_set.first().item_type == 'Book Section'

    ### Test Case 2
    # Three copies of Émile ou de l'éducation by Rousseau, some with
    # accents in the titles and some without
    rousseau_works = Work.objects.filter(authors__authorized_name__contains='Rousseau')
    rousseau_instances = Instance.objects.filter(work__authors__authorized_name__contains='Rousseau')
    assert rousseau_works.count() == 1
    assert rousseau_instances.count() == 3
    assert rousseau_works.first().year == 1966

    ## Test Case 3
    # Journal article; test that all data is copied
    article_work = Work.objects.get(authors__authorized_name__contains='Barthes')
    article = Instance.objects.get(work__authors__authorized_name__contains='Barthes')
    assert article.item_type == 'Journal Article'
    assert article.journal.name == 'Communications'
    assert article.start_page == '40'
    assert article.end_page == '51'
    assert article_work.primary_title == "Rhétorique de l'image"
    assert article_work.short_title == "Rhétorique de l'image"
    # fixture modified to test second place of publication
    assert article.pub_place.count() == 2
    assert article.pub_place.all()[0].name == 'Paris'
    assert article.pub_place.all()[1].name == 'Princeton, NJ'
    assert 'interesting discrepancy' in article.notes
    assert article.copyright_year == 1964
    assert article.is_extant
    assert article.is_annotated
    assert not article.is_translation
    assert not article.has_insertions
    assert not article.has_dedication
    assert article.uri == "http://findingaids.princeton.edu/collections/RBD1.1/c478"
    # fixture modified to test pub date
    assert article.print_date.isoformat() == "1964-01-01"
    assert not article.print_date_day_known
    assert not article.print_date_month_known
    # references copied
    assert article.reference_set.count() == 2

    # Test Case 4
    # data modified to force page range parsing error
    instance = Instance.objects.get(work__primary_title__contains='Le Petit')
    assert 'Error parsing page range "foo-bar"' in instance.notes

