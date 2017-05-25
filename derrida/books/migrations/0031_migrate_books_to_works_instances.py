# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-18 19:14
from __future__ import unicode_literals
import re

from django.db import migrations

from derrida.books.migration_utils import cleaned_title, belongs_to_work, \
    parse_page_range


def books_to_works_instances(apps, schema_editor):
    # import historical versions of the models as they exist
    # at this point in the migrations to convert data
    # from books into works and associated instances
    Book = apps.get_model("books", "Book")

    # group books first! then create works
    # sort by title/author?

    # process full books first, in hopes of creating collected work
    # records first before processing book sections
    books_to_works(Book.objects.filter(item_type__name='Book'), apps)
    # then process all the other books
    books_to_works(Book.objects.exclude(item_type__name='Book'), apps)


def books_to_works(books, apps):
    # expect a books queryset that can be ordered and sorted

    # sort books by primary title, then by author
    books = books.order_by('primary_title')
            # return self.creator_set.filter(creator_type__name='Author')
    books = sorted(books,
        key=lambda book: list(book.creator_set.filter(creator_type__name='Author').values_list()))

    Work = apps.get_model("books", "Work")
    WorkSubject = apps.get_model("books", "WorkSubject")
    WorkLanguage = apps.get_model("books", "WorkLanguage")
    Instance = apps.get_model("books", "Instance")
    InstanceCatalogue = apps.get_model("books", "InstanceCatalogue")
    InstanceLanguage = apps.get_model("books", "InstanceLanguage")
    Place = apps.get_model("places", "Place")

    previous_work = None

    # books are grouped in such a way that detectable matching instances
    # should be processed in order
    for book in books:
        # capture author list, may be used in multiple places
        book_authors = [creator.person for creator in
                        book.creator_set.filter(creator_type__name='Author')]

        if previous_work and belongs_to_work(book, previous_work):
            work = previous_work
            # no guarantee we get works in order; if current instance
            # copyright year is later than current work year, update the work
            if not work.year or (book.copyright_year and work.year > book.copyright_year):
                work.year = book.copyright_year
                work.save()

        # otherwise, create a new work
        else:
            work_title = cleaned_title(book.primary_title, remove_accents=False)
            work = Work.objects.create(primary_title=work_title,
                short_title=work_title,
                year=book.work_year or book.copyright_year)
            # NOTE: work_year doesn't seem to be set; use copyright year
            # as a placeholder
            work.authors.set(book_authors)
            # subjects could include flags for primary or notes, so
            # create via through model
            WorkSubject.objects.bulk_create([
                WorkSubject(work=work, subject=booksubj.subject,
                            is_primary=booksubj.is_primary,
                            notes=booksubj.notes)
                for booksubj in book.booksubject_set.all()])
            # similar for languages
            WorkLanguage.objects.bulk_create([
                WorkLanguage(work=work, subject=booklang.language,
                            is_primary=booklang.is_primary,
                            notes=booklang.notes)
                for booklang in book.booklanguage_set.all()])

            # store the new work to check for re-use when processing the next book
            previous_work = work

        # then create the individual instance
        instance = Instance.objects.create(work=work)
        # NOTE: this migration doesn't set alternate title because
        # items with alternate titles can't be grouped into works;
        # those items will require manual cleanup

        # these fields copy exactly from book to work unchanged
        copy_fields = ['publisher', 'zotero_id', 'is_extant', 'is_annotated',
                       'is_translation', 'dimensions', 'copyright_year',
                       'journal', 'uri', 'has_dedication', 'has_insertions',
                       'notes']
        for field in copy_fields:
            setattr(instance, field, getattr(book, field))
        # convert book ambiguous pub date to instance print date
        instance.print_date = book.pub_date
        instance.print_date_day_known = not book.pub_day_missing
        instance.print_date_month_known = not book.pub_month_missing

        # publication place - now multiple
        if book.pub_place:
            instance.pub_place.add(book.pub_place)
        # second pub place, if any, is stored in original pub info
        # (only known case in initial data uses & to combine locations)
        if book.original_pub_info and '&' in book.original_pub_info:
            second_place = book.original_pub_info.split(' & ')[1]
            instance.pub_place.add(Place.objects.get(name=second_place))

        # convert page range to start/end
        if book.page_range:
            try:
                start, end = parse_page_range(book.page_range)
                instance.start_page = start
                instance.end_page = end
            except:
                # if page range couldn't be parsed, add a note
                instance.notes += '\Error parsing page range "%s"' % \
                    book.page_range

        # set instance languages
        InstanceLanguage.objects.bulk_create([
            InstanceLanguage(instance=instance, subject=booklang.language,
                        is_primary=booklang.is_primary,
                        notes=booklang.notes)
            for booklang in book.booklanguage_set.all()])

        # copy catalogu data from book to instance
        for catalog_record in book.catalogue_set.all():
            instance.instancecatalogue_set.add(InstanceCatalogue.objects.create(
                instance=instance,
                institution=catalog_record.institution,
                is_current=catalog_record.is_current,
                call_number=catalog_record.call_number
            ))

        # if item is a book sections, related new instance to the instance
        # that includes/collects it
        if book.larger_work_title and book.item_type.name == 'Book Section':
            matches = Instance.objects.filter(work__primary_title=book.larger_work_title,
                work__authors__in=book_authors)
            if matches.exists() and matches.count() == 1:
                collection = matches.first()
            else:
                collection_work = Work.objects.create(primary_title=book.larger_work_title,
                    short_title=book.larger_work_title,
                    year=book.work_year or book.copyright_year,
                    notes='Stub collection work %s created from book section for %s' % \
                        (book.larger_work_title, book.short_title))
                collection_work.authors.set(book_authors)
                collection = Instance.objects.create(work=collection_work,
                    notes='Stub collection instance %s created from book section for %s' % \
                        (book.larger_work_title, book.short_title))

            instance.collected_in = collection

        instance.save()

        # find all references associated with the book and associate
        # with the new instance
        instance.reference_set.set(book.reference_set.all())

        # NOTE: generic relation footnote is not accessible;
        # this migration will ignore them and not copy over from
        # books to corresponding instances
        # associate any footnotes
        # (if we needed to handle: find footnotes that belong to this
        # book and update object id and content type)


def remove_works_instances(apps, schema_editor):

    Work = apps.get_model("books", "Work")
    Instance = apps.get_model("books", "Instance")

    Instance.objects.all().delete()
    Work.objects.all().delete()


# TODO: reverse migration: delete all works and instances (?)

class Migration(migrations.Migration):

    dependencies = [
        ('books', '0030_split_book_into_work_instance'),
    ]

    operations = [
            migrations.RunPython(books_to_works_instances, remove_works_instances),
    ]
