derrida-django
==============

.. sphinx-start-marker-do-not-remove

Django web application for `Derrida's Margins <https://derridas-margins.princeton.edu/>`_
a `DH project sponsored by CDH <https://cdh.princeton.edu/projects/derridas-margins/>`_.

.. image:: https://travis-ci.org/Princeton-CDH/derrida-django.svg?branch=develop
   :target: https://travis-ci.org/Princeton-CDH/derrida-django
   :alt: Build status

.. image:: https://landscape.io/github/Princeton-CDH/derrida-django/develop/landscape.svg?style=flat
  :target: https://landscape.io/github/Princeton-CDH/derrida-django/develop
  :alt: Code Health

.. image:: https://codecov.io/gh/Princeton-CDH/derrida-django/branch/develop/graph/badge.svg
   :target: https://codecov.io/gh/Princeton-CDH/derrida-django
   :alt: Code coverage

.. image:: https://requires.io/github/Princeton-CDH/derrida-django/requirements.svg?branch=develop
   :target: https://requires.io/github/Princeton-CDH/derrida-django/requirements/?branch=develop
   :alt: Requirements Status

`Current release documentation <https://princeton-cdh.github.io/derrida-django/>`_.

This repository uses `git-flow <https://github.com/nvie/gitflow>`_ conventions; master
contains the most recent release, and work in progress will be on the develop branch.
Pull requests should be made against develop.


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


Unit Tests
~~~~~~~~~~

Unit tests are written with `py.test <http://doc.pytest.org/>`_ but use
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

Documentation
~~~~~~~~~~~~~

Documentation is generated using `sphinx <http://www.sphinx-doc.org/>`__
To generate documentation, first install development requirements::

    pip install -r dev-requirements.txt

Then build the documentation using the customized make file in the `docs`
directory::

    cd sphinx-docs
    make html

When building documentation for a production release, use `make docs` to
update the published documentation on GitHub Pages.
