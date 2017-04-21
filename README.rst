derrida-django
--------------
Django web application for the `Derrida's Margins Project
<https://cdh.princeton.edu/projects/derridas-margins/>`_.

.. image:: https://travis-ci.org/Princeton-CDH/derrida-django.svg?branch=develop
   :target: https://travis-ci.org/Princeton-CDH/derrida-django
   :alt: Build status

.. image:: https://landscape.io/github/Princeton-CDH/derrida-django/develop/landscape.svg?style=flat
  :target: https://landscape.io/github/Princeton-CDH/derrida-django/develop
  :alt: Code Health

.. image:: https://codecov.io/gh/Princeton-CDH/derrida-django/branch/develop/graph/badge.svg
   :target: https://codecov.io/gh/Princeton-CDH/derrida-django
   :alt: Code coverage



This repo uses `git-flow <https://github.com/nvie/gitflow>`_ conventions, so the
most recent code will be on the develop branch.

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

-  recommended: create and activate a python 3.5 virtualenv
   ``virtualenv derrida -p python3.5`` ``source derrida/bin/activate``

-  pip install required python dependencies
   ``pip install -r requirements.txt``
   ``pip install -r dev-requirements.txt``

-  copy sample local settings and configure for your environment
   ``cp derrida/local_settings.py.sample derrida/local_settings.py``

(documentation TODO) - install & configure git commit hook for Asana
integration

Unit Tests
~~~~~~~~~~

Unit tests are written with `py.test <http://doc.pytest.org/>`__ but use
Django fixture loading and convenience testing methods when that makes
things easier. To run them, first install development requirements::

    pip install -r dev-requirements.txt

Run tests using py.test::

    py.test

Deploy
~~~~~~

We include sample deploy scripts in the form of a short `Ansible <http://docs.ansible.com/>`__ playbook
and associated configuration files. In the current usage, assuming Ansible
is installed and the appropriate server key is loaded via `ssh-add`::

    cd derrida-django/deploy/
    ansible-playbook prod_derrida-django_.yml <-e github reference>

Any valid Github tag type is accepted, but the script defaults to `master`.
`ansible.cfg` and `hosts` set up the host group and configuration used in the
commands.

Documentation
~~~~~~~~~~~~~

Documentation is generated using `sphinx <http://www.sphinx-doc.org/>`__
To generate documentation them, first install development requirements::

    pip install -r dev-requirements.txt

Then build documentation using the customized make file in the `docs`
directory::

    cd docs
    make html

You can also view documentation for the current master branch `on GitHub Pages <https://princeton-cdh.github.io/derrida-django/html/>`__
