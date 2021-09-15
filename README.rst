derrida-django
==============

.. sphinx-start-marker-do-not-remove

Django web application for `Derrida's Margins <https://derridas-margins.princeton.edu/>`_
a `DH project sponsored by CDH <https://cdh.princeton.edu/projects/derridas-margins/>`_.

.. image:: https://zenodo.org/badge/83320273.svg
   :target: https://zenodo.org/badge/latestdoi/83320273
   :alt: DOI: 10.5281/zenodo.1299972

.. image:: https://github.com/Princeton-CDH/derrida-django/actions/workflows/unittests.yaml/badge.svg
    :target: https://github.com/Princeton-CDH/derrida-django/actions/workflows/unittests.yaml
    :alt: Unit Test status

.. image:: https://codecov.io/gh/Princeton-CDH/derrida-django/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/Princeton-CDH/derrida-django
   :alt: Code coverage

.. image:: https://api.codeclimate.com/v1/badges/1cb1a007da663863e326/maintainability
   :target: https://codeclimate.com/github/Princeton-CDH/derrida-django/maintainability
   :alt: Maintainability

.. image:: https://requires.io/github/Princeton-CDH/derrida-django/requirements.svg?branch=main
   :target: https://requires.io/github/Princeton-CDH/derrida-django/requirements/?branch=main
   :alt: Requirements Status

`Current release documentation <https://princeton-cdh.github.io/derrida-django/>`_.

This repository uses `git-flow <https://github.com/nvie/gitflow>`_ conventions; main
contains the most recent release, and work in progress will be on the develop branch.
Pull requests should be made against develop.

Python 3.5 / Django 1.11 / Node 8.16.0 / MariaDB (MySQL) 5.5 w/ timezone info

License
-------

**derrida-django** is distributed under the Apache 2.0 License.

©2018 Trustees of Princeton University.  Permission granted via
Princeton Docket #18-3472-1 for distribution online under a standard Open Source
license.  Ownership rights transferred to Rebecca Koeser provided software
is distributed online via open source.

Development instructions
------------------------

Initial setup and installation:

-  **recommended:** create and activate a python 3.5 virtualenv::

     virtualenv derrida -p python3.5
     source derrida/bin/activate

-  Use pip to install required python dependencies::

     pip install -r requirements.txt
     pip install -r dev-requirements.txt

-  Copy sample local settings and configure for your environment::

     cp derrida/local_settings.py.sample derrida/local_settings.py

- Download required fonts from project folder and add to `/sitemedia/fonts`

- Create a database, configure in local settings, and run migrations::

    python manage.py migrate

- Create a Solr core, configure it, and index content::

    python manage.py build_solr_schema --configure-directory=/path/to/solr/derrida/conf --reload-core derrida
    python manage.py rebuild_index --noinput

- If running this application on MariaDB/MySQL, you must make sure that
  time zone definitions are installed. On most flavors of Linux/MacOS,
  you may use the following command, which will prompt
  for the database server's root password::

    mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql -p

  If this command does not work, make sure you have the command line utilities
  for MariaDB/MySQL installed and consult the documentation for your OS for
  timezone info. Windows users will need to install a copy of the zoneinfo
  files.

  See `MariaDB <https://mariadb.com/kb/en/library/mysql_tzinfo_to_sql/>`_'s
  info on the utility for more information.

Tests
~~~~~

Python unit tests are written with `py.test <http://doc.pytest.org/>`_ but use
Django fixture loading and convenience testing methods when that makes
things easier. To run them, first install development requirements::

    pip install -r dev-requirements.txt

Configure a Solr core for testing and update with the built solr schema
using the same build_solr_schema manage command as for development, above.
(The test Solr core will be cleared and reindexed for tests of functionality
that require Solr.)  Any new unit tests that require Solr should use Django
`override_settings` to use the test connection.

Run tests using py.test::

    py.test

Automated accessibility testing is also possible using `pa11y <https://github.com/pa11y/pa11y>`_
and `pa11y-ci <https://github.com/pa11y/pa11y-ci>`_. To run accessibility tests,
start the server with ``python manage.py runserver`` and then use ``npm``::

    npm run pa11y

The accessibility tests are configured to read options from the ``.pa11yci.json``
file and look for a sitemap at ``localhost:8000/sitemap.xml`` to use to crawl the
site. Additional URLs to test can be added to the `urls` property of the
``.pa11yci.json`` file.

Data
----

To generate the published datasets, run the following commands::

    python manage.py annotation_data
    python manage.py instance_data
    python manage.py insertion_data
    python manage.py reference_data

To ensure that the data conforms to our requirements, run the 
`Frictionless Data <https://frictionlessdata.io/>`_ test::

    frictionless validate datapackage.json


Documentation
-------------

Documentation is generated using `sphinx <http://www.sphinx-doc.org/>`_.
To generate documentation, first install development requirements::

    pip install -r dev-requirements.txt

Then build documentation using the customized make file in the `docs`
directory::

    cd sphinx-docs
    make html

To build and publish documentation for a release, add the ``gh-pages`` branch
to the ``docs`` folder in your worktree::

  git worktree add -B gh-pages docs origin/gh-pages

In the ``sphinx-docs`` folder, use ``make docs`` to build the HTML documents
and static assets, add it to the docs folder, and commit it for publication on
Github Pages. After the build completes, push to GitHub from the ``docs`` folder.
