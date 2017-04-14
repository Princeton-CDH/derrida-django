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

import_nysl
^^^^^^^^^^^
.. automodule:: derrida.books.management.commands.import_nysl

  Import command for derrida team's spreadsheet. It can be invoked using::

    python manage.py import_nysql [--justsammel] /path/to/csv

  The ``--justsammel`` flag skips import of records to avoid
  reproducing duplicates, but rebuilds the ```is_sammelband`` flag set and
  produces an output list.

  The expect behavior is designed for a once-off import and will produce
  duplicate book entries (but not duplicates of any entries created
  as part of book creation).

  All persons created attempt to have a VIAF uri associated and all places
  have a Geonames ID assigned if possible.

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
