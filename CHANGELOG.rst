.. _CHANGELOG:

CHANGELOG
=========

0.9 (Library works and references)
----------------------------------

Library works
~~~~~~~~~~~~~

* As a record editor, I want to mark a copy of edition in order to differentiate when two exact copies were in Derrida's library.
* As a user, I want to view a paginated list of books in Derrida's library that are cited in Derrida's works so that I can engage with the materials he referenced in his writing.
* As a user, I want to filter the list of books cited in Derrida's works so that I can narrow the list based on my interests.
* As a user, I want to see an indication of which library books in the list are annotated so I can easily identify books with annotations.
* As a user, I want to change how the list of books is sorted so that I can browse the list in different ways.
* As a user looking at a single book in the library, I want to see a list of other copies and editions of the same work so that I can see all the versions Derrida cited.
* As a user looking at a single book in the library, I want to see a gallery of images for that book so that I see what it looks like and see sample annotated pages.
* As a user, I want to optionally select one content type so that I can restrict my search to a single set of materials on the site.
* As a user, I want to search across library works, references, interventions, and essays so that I can find content that interests me across types of material.
* As an admin I need a way to take down book or page images so that I can comply quickly with any requests from copyright holders.
* As an admin, I want to edit content pages so that I can manage and update site content without developer assistance.
* As a user I want to see a larger view of book images with any captured annotations so that I can see images in more detail.
* As a user, I want to be able to search on French terms with or without accents so that I can easily find items with French text.
* As an admin, I want to edit descriptions for dynamic list pages so that I can update wording without developer intervention.
* As an admin, I want to manage pages in site navigation so I can update order and labels without developer intervention.
* As an admin, I want to create and edit outwork content so that I can post essays and other content on the site.
* As a user, I want to see the bibliographic details for a single book in Derrida's library so I can see what edition it is and where to get it.

References and interventions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* As a record editor, I want to document page ranges for chapters in Derrida's works so that references on the site can be filtered and displayed by chapter.
* As a user, I want to view a paginated list of references in Derrida's works so that I can see the extent and range of references he made to materials in his library
* As a user, I want to see a visualization of references by chapter in Derrida's work so that I can get a sense of how references are distributed through the work.
* As a user, I want to see a visualization of references by author of referenced work so that I can get a sense of distribution by cited author.
* As a user looking at a single book, I want to see the references to that work so I can get a sense of how Derrida used it.
* As a user, I want to filter the list of references so that I can narrow the results based on my interests.
* As a user, I want to change how the list of references is sorted so that I can browse the list in different ways.
* As a user searching across all site materials, I want to access all results for a single kind of item so that I can see more results.
* As a user searching library works or references, I want to use the same filters and sort options as when I browse so that I can narrow my search results.
* As a user, I want to filter intervention search results so that I can narrow the results by aspects of the annotation or annotated work.
* As a user looking at a single book, I want the option to sort references by page order in Derrida work or referenced book so that I can see them in either order.
* As a user, I should only see large images of annotated pages, overview images, and insertions because the material is still under copyright.
* As a user, I want to search across interventions so I can see the kinds of marks and other interventions made in Derrida's Library.
* As a user, I want to filter intervention search results so that I can narrow the results by aspects of the annotation or annotated work.
* As a user, I want the option to sort interventions by author or title of annotated work so I can look at them in different ways.
* As a user I want to visualize and filter years by range so I can get an idea of the distribution and filter items by ranges of years.
* As a user, I want a way to link directly to a specific annotation so that I can cite or share that annotation.

Other improvements
~~~~~~~~~~~~~~~~~~
* Migrate IIIF canvas urls from plum to figgy (Princeton University Library IIIF service)
* Migrate books to reassociate collection references with book section by chapter
* Serve IIIF images based on nearest pre-generated size from IIIF server

0.8.1
-----
Maintenance release to provide needed migration

0.8 (Interventions Phase I)
---------------------------
Release implementing the first part of the interventions interface, allowing
data editors to note Derrida's annotation-style interventions on digital editions
of his library works.

Access
~~~~~~

* As a record editor, I can only view digitized materials from Derrida's library when I am logged in so that copyrighted materials are not exposed to the general public.
* As a logged in record editor, I should be able to create an intervention record so that I can document Derrida's interventions in the works in his library.
* As a logged in record editor, I should be able to view, edit, and delete all intervention records (no matter who created them) so that I can manage all documented interventions in Derrida's library.
* Logged in record editors or anyone with greater permissions should be able to view the books; anonymous users or logged in users without those permissions should not.
* As an admin, I want to see the history of all edits to an intervention, including edits made via the canvas image interface, so that I can track who has contributed and made changes to the data.

Books
~~~~~

* As a record editor, when I’m editing a book record I want to see a list of all the interventions (annotations and insertions) associated with that book so that I can review and update interventions by related book.
* As a record editor, when I’m editing a book I want to be able to view the associated digitized materials so I can see pictures of the book, annotations, insertions, and other relevant markings.
* As a record editor, I want to see an indicator if a library instance has a digital edition associated and be able to sort on the presence of a digital edition so that I can easily get to volumes that have been digitized.

Citations
~~~~~~~~~

* As a record editor, I want to be able to associate a citation with one or more interventions (annotations or insertions) so that I can identify instances where citations relate in an explicit way to interventions (for example, a passage is quoted in the Derrida text and underlined in the book from the library).
* As a record editor, when editing this field in the Django admin, I want it to automatically filter to only those intervetions associated with the digital edition of the book (i.e. if a reference is set to BookA, only interventions associated with BookA show up).

Interventions
~~~~~~~~~~~~~

* As an intervention data editor, I want the option of leaving all fields blank so that I can accurately describe non-verbal interventions or interventions that don't relate to anchor text.
* As an intervention data editor, I want to be able to add and edit the color if the ink type is “pen," so that I can see if there are patterns in Derrida's pen usage and whether he revisited the same text.
* As an interventions data editor, I want to select non-verbal interventions (underlining, circling, etc.) on a page image so I can transcribe anchor text and document the intervention and where it occurs.
* As an intervention data editor, I want to edit any of the text fields (transcription, translation, anchor text, tags etc) so that I can correct mistakes or make updates.
* As an intervention data editor, I want to select verbal interventions on a page image and enter a transcription of the text so I can document the intervention and where it occurs.
* As a data editor, I want to see an indicator on the Django admin site that shows whether an intervention is verbal or non-verbal, so I can more easily distinguish these important categories.
* As an intervention data editor, I would like to be able to tag part or all of transcribed verbal intervention text as “uncertain.”
* As an intervention data editor, I would like to be able to tag a verbal intervention as “illegible” so that I can clearly indicate when the text is unreadable.
* As an interventions data editor, I want the option to enter a translation of verbal intervention text so that I can provide an English version when the original is in another language.
* As an interventions data editor, I want to associate an intervention with the person who wrote it so that I can document the author when that information is known; I want “Derrida, Jacques” to be the default intervention author, and I want to be able to add or edit this information.
* As an interventions data editor, I want to document the language of anchor text and annotation text so that I can track use of languages across interventions.
* As an intervention data editor, I want to transcribe the anchor text (if there is any) for an annotation so I can document the text the intervener is referencing.
* As an intervention data editor, I want to tag interventions from a pre-defined list so that I can describe the characteristics and type of intervention.
* As a record editor I want to view, edit, and create tags to describe and annotations and insertions so that I can manage the tags available for interventions.


0.7
---

Maintenance release to clean up obsolete models and code after
the refactor in 0.6.

* Fix footnote object lookup so it is restricted to models that can
  be listed in Django admin.
* Remove obsolete code (Book models, Zotero book import) and dependencies,
  and squash book migrations


0.6 Bibliographic Enhancements
------------------------------

Refactor books into works and instances; update citation admin functionality to support capturing citation anchor text with minimal formatting.

* As a record editor, I want to be able to add new or edit citation anchor text in both French and English.
* As an data editor, I want to be able to add the anchor text of a citation along with basic markdown formatting (bold, italic) so that I can accurately capture Derrida's citations.
* As a record editor, I want to add and edit bibliographic data for works and instances of works so I can document shared metadata and group different copies and editions of the same work.
* As a record editor, I want to document the print date for a book, including month and year when available, so that I can check if a given copy was available to Derrida when he was writing a text.


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

Footnotes
~~~~~~~~~

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
