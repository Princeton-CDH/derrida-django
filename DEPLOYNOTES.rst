.. _DEPLOYNOTES:

Deploy and Upgrade notes
========================

0.8 Interventions Phase I
-------------------------

* This release adds `django.contrib.sites` to **INSTALLED_APPS**, so you
  will need to manually configure your site domain in Django admin.
* An auth token must be configured using **DJIFFY_AUTH_TOKENS** in
  ``local_settings.py`` in order to import restricted IIIF manifests.
* To load IIIF digitized content for documenting interventions, you should use
  the **import_digitaleds** manage.py script. Use **PUL** to load the
  entire collection::

    python manage.py import_digitaleds PUL

Ansible
~~~~~~~

We include sample deploy scripts in the form of a short `Ansible <http://docs.ansible.com/>`__ playbook
and associated configuration files. In the current usage, assuming Ansible
is installed and the appropriate server key is loaded via `ssh-add`::

    cd derrida-django/deploy/
    ansible-playbook prod_derrida-django_.yml <-e github reference>

Any valid Github tag type is accepted, but the script defaults to ``master``. ``ansible.cfg`` and ``hosts`` set up the host group and configuration used in the commands.

The production deploy does not involve itself with Apache configuration, because
that is handled server side and now handles running a database backup, migrations,
and resetting symlinks to make the deployment go live.
