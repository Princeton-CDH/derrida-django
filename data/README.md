# Dataset Documentation

Details for each field can be found in the [datapackage.yaml](datapackage.yaml)

## Annotations

A collection of all written annotations in Jacques Derrida's library

* Files: [annotations.csv](annotations.csv), [annotations.json](annotations.json)
* Number of fields: 16
* Number of rows: 1,420

**Field List:**
* `id` : Unique identifier linking to the annotation's page
* `book_id` : Link to the book where the annotation was found
* `book_title` : Title of the book where the annotation was found
* `book_type` : Whether the work is a full book or a section of a book.
* `page` : The page where the annotation was found
* `tags` : Supplemental information about the annotation (e.g. blue ink, arrow)
* `text_content` : Words included in the annotation
* `text_language` : The language used in the annotation
* `text_language_code` : The ISO 639-1 codes for the language used in the annotation
* `text_translation` : Translation of the annotation text
* `quote_content` : The book's text that was highlighted or underlined by the given annotation
* `quote_language` : The language of the book's text that was highlighted by the annotation
* `quote_language_code` : The ISO 639-1 codes for the book's text that was highlighted by the annotation
* `annotator` : The person who made the annotation
* `annotation_region` : A link to the IIIF image of the book's page that has been cropped to show just the given annotation
* `page_iiif` : A link to the IIIF image of the book's page

## References

References to other works made in Jacques Derrida's 1967 book *De la grammatologie*

* Files: [references.csv](references.csv), [references.json](references.json)
* Number of fields: 12
* Number of rows: 1,052

**Field List**
* `id` : An identifier linking to the reference's detail page. Note that these are not unique.
* `page` : The page in De la grammatologie where the reference was cited
* `page_location` :
* `type` : How Derrida references the work (e.g. via a footnote, a quotation, etc.)
* `book_title` : The title of the book referenced
* `book_id` : Link to the book where the reference was found
* `book_page` : Page of the book in Derrida's citation
* `book_type` : Whether or not the reference is to a book or journal article
* `anchor_text` : The text of the quotation or the footnote that makes up the reference
* `interventions` : A URI to the linked annotation (if Derrida had a book where this reference was annotated.)
* `section` : Section of De la grammatologie where the reference is located
* `chapter` : Chapter of De la grammatologie where the reference is located

## Library

Books from Derrida's personal library

* Files: [library.csv](library.csv), [library.json](library.json)
* Number of fields: 28
* Number of rows: 222

**Field List**
* `id` : Unique link to the book's detail page
* `item_type` : The type of work (either a book, journal article, or book section)
* `title` : Title of the given work
* `alternate_title` :
* `work_year` : Year in which the work was published
* `copyright_year` : Year in which the work was copyrighted
* `print_date` : Print date of the work
* `authors` : Authors of the work
* `contributors` : Known contributors to the work (e.g translators or editors)
* `publisher` : Publisher of the work
* `pub_place` : City in which the work was published
* `is_extant` : Work exists in Derrida's library
* `is_annotated` : The instance was annotated
* `is_translation` : The work is a translation
* `has_dedication` :
* `has_insertions` : The instance contains insertions
* `copy` :
* `dimensions` : Dimensions of the instance in Derrida's library
* `subjects` : The subjects covered in the work
* `languages` : The languages covered in the work
* `journal_title` : The name of the journal in which the journal article was published
* `collected_work_title` : The title of the work in which the given item is collected
* `collected_work_uri` : The URI of the work in which the given item is collected
* `start_page` : Start page of the work, often within a collected work
* `end_page` : End page of the work, often within a collected work
* `has_digital_edition` :
* `catalog_uri` : A link to the instance in Princeton University Library's finding aids catalog
* `zotero_id` : The work's Zotero ID

## Insertions

Physical insertions placed inside books in Derrida's library

* Files: [library.csv](library.csv), [library.json](library.json)
* Number of fields: 8
* Number of rows: 251

**Field List**
* `id` : A unique identifier for the given insertion
* `book_id` : Link to the book where the insertion was found
* `book_title` : Title of the book where the insertion was found
* `book_type` : Whether the insertion was found in a book or journal article
* `page` : Page on which the insertion was found
* `num_images` : The number of images that make up the insertion
* `image_labels` : Description of the images that make up the insertion
* `image_iiif` : A semicolon-delimited list of IIIF links to the insertion images