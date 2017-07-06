import re
from unidecode import unidecode

## NOTE: this code will be removed once squashed book migrations. ##
## have been applied and old migration code is removed.           ##


def cleaned_title(title, remove_accents=True):
    # remove parenthetical or bracketed comments at the end of a title
    # for comparison purposes;
    # convert accented characters to plain text equivalent so that
    # variants with and without accents will match
    title = re.sub(r'\s*[\[\()].*[\]\)]\s*$', '', title)
    if remove_accents:
        return unidecode(title)
    return title


def belongs_to_work(book, work):
    # a book belongs to a work IF
    # - all authors match AND
    #   titles match exactly (case-insensitive)
    #  OR titles match after dropping parenthetical/bracket of book title

    work_title = cleaned_title(work.primary_title.strip().lower())
    book_title = cleaned_title(book.primary_title).strip().lower()
    # NOTE: not using convenience method book.authors because this utility
    # is intended for use with migration models which do not have
    # access to custom mdoel methods
    book_authors = [creator.person for creator in
                    book.creator_set.filter(creator_type__name='Author')]

    return work.authors.count() == len(book_authors) and \
        all([person in work.authors.all() for person in book_authors]) \
        and book_title == work_title


def parse_page_range(page_range):
    # match digits or roman numerals
    re_page_num = re.compile(r'^[\dIVXLDM]+$')

    # page range
    if '-' in page_range:
        pages = page_range.split('-')
        if all([re_page_num.match(pg) for pg in pages]):
            return pages
    # single page
    if re_page_num.match(page_range):
        return [page_range, page_range]

    # error if not parsable as page range
    raise Exception('Failed to parse page range')

