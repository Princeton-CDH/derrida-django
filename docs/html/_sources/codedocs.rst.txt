Code Documentation
==================

.. toctree::
   :maxdepth: 2

Common
------
.. automodule:: derrida.common
    :members:

Models
^^^^^^
.. automodule:: derrida.common.models
    :members:

Places
-------
.. automodule:: derrida.places
    :members:

Models
^^^^^^
.. automodule:: derrida.places.models
    :members:

Views
^^^^^
.. automodule:: derrida.places.views
    :members:

GeoNames
^^^^^^^^
.. automodule:: derrida.places.geonames
    :members:

Books
-----
.. automodule:: derrida.books
    :members:

Models
^^^^^^
.. automodule:: derrida.books.models
    :members:

Views
^^^^^
.. automodule:: derrida.books.views
    :members:

import_zotero
^^^^^^^^^^^^^
.. automodule:: derrida.books.management.commands.import_zotero

  Import command for derrida team's spreadsheet. It can be invoked using::

    python manage.py import_zotero /path/to/csv

  The expect behavior is designed for a once-off import of entries exported
  from a Zotero library and will produce
  duplicate book entries (but not duplicates of any entries created
  as part of book creation).

  All persons created attempt to have a VIAF uri associated and all places
  have a Geonames ID assigned if possible.

The tag schema used by the team was:

1. Derrida’s work title: (always dg)
2. Page number in ``DG``: arabic numeral
3. position of reference on page in sequential order from top to bottom: lower case letter (``a, b, c, d`` etc.)
4. Type of reference in ``DG``: ``C, Q, F or E`` (citation, quotation, footnote, or epigraph.)
5. page number in cited work: arabic numeral (pending clarification of what to do with roman numerals)
6. whether Derrida cites the page number alone or appended with sq. : if alone, this field has ``p``, if sq., this field has ``s``
7. whether our copy of Derrida’s cited work exists in the library and if so, whether it has annotations: ``Y / N / U`` (yes, we have it and it has annotations; we have it but the page cited doesn’t have annotations; we don’t have the work in Derrida’s library)

e.g. ``dg11aQ256pY`` could be a reference contained in the first position on p. 11 of DG and containing a quotation from p. 256 of the cited work that exists in Derrida’s library and contains annotations on p. 256.
``dg11aQ_is`` a provisional tag that could be created based only on the information contained within DG.


People
------
.. automodule:: derrida.people
    :members:

Models
^^^^^^
.. automodule:: derrida.people.models
    :members:

Views
^^^^^
.. automodule:: derrida.people.views
    :members:

VIAF
^^^^^
.. automodule:: derrida.people.viaf
    :members:

Footnotes
---------
.. automodule:: derrida.footnotes
    :members:

Models
^^^^^^
.. automodule:: derrida.footnotes.models
    :members:
