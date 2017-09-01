derrida-django
==============

.. sphinx-start-marker-do-not-remove

Django web application for the `Derrida's Margins Project
<https://cdh.princeton.edu/projects/derridas-margins/>`_.

.. image:: https://travis-ci.org/Princeton-CDH/derrida-django.svg?branch=master
   :target: https://travis-ci.org/Princeton-CDH/derrida-django
   :alt: Build status

.. image:: https://landscape.io/github/Princeton-CDH/derrida-django/master/landscape.svg?style=flat
  :target: https://landscape.io/github/Princeton-CDH/derrida-django/master
  :alt: Code Health

.. image:: https://codecov.io/gh/Princeton-CDH/derrida-django/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Princeton-CDH/derrida-django
   :alt: Code coverage

.. image:: https://requires.io/github/Princeton-CDH/derrida-django/requirements.svg?branch=master
   :target: https://requires.io/github/Princeton-CDH/derrida-django/requirements/?branch=master
   :alt: Requirements Status

`Current release documentation <https://princeton-cdh.github.io/derrida-django/>`_.

This repo uses `git-flow <https://github.com/nvie/gitflow>`_ conventions; master
contains the most recent release, and work in progress will be on the develop branch.
Pull requests shoudl be made against develop.

Current development status
--------------------------

.. image:: https://badge.waffle.io/Princeton-CDH/winthrop-django.svg?label=development+in+progress&title=In+Progress
   :target: http://waffle.io/Princeton-CDH/derrida-django
   :alt: In Progress
.. image:: https://badge.waffle.io/Princeton-CDH/winthrop-django.svg?label=development+complete&title=Development+Complete
   :target: http://waffle.io/Princeton-CDH/derrida-django
   :alt: Development Complete
.. image:: https://badge.waffle.io/Princeton-CDH/winthrop-django.svg?label=awaiting+testing&title=Awaiting+Testing
   :target: http://waffle.io/Princeton-CDH/derrida-django
   :alt: Awaiting Testing


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

- Create a database, configure in local settings, and run migrations::

    python manage.py migrate

- Create a Solr core, configure it, and index content::

  python manage.py build_solr_schema --configure-directory=/path/to/solr/derrida/conf --reload-core derrida
  python manage.py rebuild_index --noinput


Unit Tests
~~~~~~~~~~

Unit tests are written with `py.test <http://doc.pytest.org/>`__ but use
Django fixture loading and convenience testing methods when that makes
things easier. To run them, first install development requirements::

    pip install -r dev-requirements.txt

Configure a Solr core for testing and update with the built solr schema.
(The test Solr core will be cleared and reindexed for tests of functionality
that require Solr.)

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
