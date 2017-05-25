import re
from unidecode import unidecode


def cleaned_title(title):
    # remove parenthetical or bracketed comments at the end of a title
    # for comparison purposes;
    # convert accented characters to plain text equivalent so that
    # variants with and without accents will match
    return unidecode(re.sub(r'\s*[\[\()].*[\]\)]\s*$', '', title))


def belongs_to_work(book, work):
    # a book belongs to a work IF
    # - all authors match AND
    #   titles match exactly (case-insensitive)
    #  OR titles match after dropping parenthetical/bracket of book title
    work_title = work.primary_title.strip().lower()
    return work.authors.count() == book.authors().count() and \
        all([creator.person in work.authors.all() for creator in book.authors()]) \
        and (book.primary_title.strip().lower() == work_title \
             or cleaned_title(book.primary_title).strip().lower() == work_title)

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

