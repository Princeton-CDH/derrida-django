.. _CHANGELOG:

CHANGELOG
=========

0.5 Bio/Bibliographical Admin interface
---------------------------------------

Initial project release implements the bio/bibliographical portion of
the database and customized Django admin interface for data import
and management of biographical and bibliographic data.

Features are expressed as user stories as written by the development and
project teams.


Book Metadata
~~~~~~~~~~~~~

* As a record editor, I want to add a new or edit an existing book so that I can document the publication data, annotation data, citations, and other relevant details.
* As a record editor, I want to add new data in or edit the following fields so that I can document them in a standard way. See `#2 <https://github.com/Princeton-CDH/derrida-django/issues/2>`__.
* As a record editor, I want to be able to add a work's original date, its copyright date, and its date d'impression (date of publication).
* As a record editor, when I’m editing a book I want to be able to associate people involved in creating the book so that I can document information about authors, translators, and editors.
* As a record editor, when I’m editing a book I want to be able to associate the book to all instances of citation related to that book.
* As a record editor, when I’m editing a book I want to be able to associate the book to a referent book (i.e., the text by Derrida in which the book is cited -- always DG at this phase).
* As a record editor, when I’m browsing the list of books I want to see the author, short title, publication year, owning institution call number, and whether a book is extant, annotated, and/or digitized so that I can get a quick overview of volumes.
* As a record editor, when I search for books in the admin interface I want to search on title, author, and notes so that I can find specific items.
* As a record editor, when I’m editing a book I want to be able to add notes about the book.


Biographic Data (People)
~~~~~~~~~~~~~~~~~~~~~~~~

* As a record editor, I want to add a new or edit an existing person so that I can document people associated with the Derrida Library.
* As a record editor, I want to add a new or edit an existing role type so that I can document the kinds of roles played by people associated with the Derrida Library.
* As a record editor, I want to add a new or edit an existing relationship type so that I can document the kinds of relationships between people associated with the Derrida Library.
* As a record editor, I want to be able to associate roles and relationships to people so that I can document how they interacted with each other and the Derrida Library.
* As a record editor, I want to be able to automatically associate authors with their VIAF URI, so that I can better document individuals associated with Derrida Library.

Footnotes **(Included under book fields in GitHub issues)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* As a data editor, I want to add a new or edit an existing source type so that I can track the kinds of source documents used as evidence in the system.
* As a data editor, I want to add a new or edit an existing footnote and associate it with any other kind of record in the system so that I can document evidence related to assertions made elsewhere in the data.
* As a data editor, when I’m editing a book or a book-person relationship, I want to be able to add footnotes on the same page so that I can add documentation on the same page.


User Management
~~~~~~~~~~~~~~~

* As a project team member, I want to login with my Princeton CAS account so that I can use existing my existing credentials and not have to keep track of a separate username and password.
* As an admin, I want to edit user and group permissions so I can manage project team member access within the system.
* As an admin, I want to edit user and group permissions so I can manage project team member access within the system.

Zotero Import
~~~~~~~~~~~~~

* As a record editor, I want a one-time import of Books from Zotero data into the system so that I can refine and augment the initial data that’s already been collected.
* As a record editor, I want a one-time import of People from Zotero data into the system so that I can refine and augment the initial data that’s already been collected.
* As a record editor, I want publishing places associated with their GeoNames ID so that I can document publishing locations more clearly.
* As a record editor, I want citations imported and associated with their works based on the tagging system implemented by the team.

KNOWN ISSUES
============

* Not all content types currently work for the footnote object number lookup in admin.
