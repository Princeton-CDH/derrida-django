# -*- coding: utf-8 -*-
import os
from unittest.mock import Mock

from django.core.management import call_command
import pytest

from derrida.people.models import Person
# Common models between projects and associated new types
from derrida.books.models import Work, Instance, CreatorType
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
    CreatorType.objects.create(name='Author')
    # NOTE: using Mock to simulate Book as a temporary measure
    # since the Book model has been removed but migration utils
    # cannot be removed yet
    book = Mock(primary_title='Essais')
    book.creator_set.filter.return_value = []

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
    book.creator_set.filter.return_value = [Mock(person=author)]
    assert migration_utils.belongs_to_work(book, work)
    # author work has more authors
    work.authors.add(author2)
    assert not migration_utils.belongs_to_work(book, work)
    book.creator_set.filter.return_value = [Mock(person=author),
        Mock(person=author2)]
    # author match with two authors
    assert migration_utils.belongs_to_work(book, work)

