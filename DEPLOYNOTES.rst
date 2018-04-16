.. _DEPLOYNOTES:

Deploy and Upgrade notes
========================


0.9
---

* Migration from Plum to Figgy requires that a new auth token be added
  to local settings under **DJIFFY_AUTH_TOKENS** for loading restricted
  IIIF Manifests.
* Solr XML configuration files ``schema.xml`` and ``solrconfig.xml``
  need to be generated and deployed to production Solr server.  Use
  ``python manage.py build_solr_schema`` to generate the schema.  Reload
  the Solr core or restart Solr after updating the configuration.
* After Solr configurations are in place, run ``python
  manage.py rebuild_index -i`` to update the index based on content
  in the Derrida database.
* Production ``local_settings.py`` should have updated settings to use the
  extended signal processor for Haystack managed models::

      HAYSTACK_SIGNAL_PROCESSOR = 'derrida.books.signals.RelationSafeRTSP'

* This update includes a migration to update cached Plum IIIF Manifest
  and Canvas data to the new equivalent Figgy URLs.  This migration
  will update records, but to update IIIF content (i.e. after additional
  labeling work), run::

    python manage.py import_digitaleds PUL --update


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
