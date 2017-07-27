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







