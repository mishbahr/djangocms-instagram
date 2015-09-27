=============================
djangocms-instagram
=============================

.. image:: http://img.shields.io/travis/mishbahr/djangocms-instagram.svg?style=flat-square
    :target: https://travis-ci.org/mishbahr/djangocms-instagram/

.. image:: http://img.shields.io/pypi/v/djangocms-instagram.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-instagram/
    :alt: Latest Version

.. image:: http://img.shields.io/pypi/dm/djangocms-instagram.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-instagram/
    :alt: Downloads

.. image:: http://img.shields.io/pypi/l/djangocms-instagram.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-instagram/
    :alt: License

.. image:: http://img.shields.io/coveralls/mishbahr/djangocms-instagram.svg?style=flat-square
  :target: https://coveralls.io/r/mishbahr/djangocms-instagram?branch=master

Use ``djangocms-instagram`` to display your latest photos or other users photos (from any non-private Instagram account), tagged photos, photos from a place or location or your liked photos.

This project requires `django-connected <https://github.com/mishbahr/django-connected>`_ and ``django-cms`` v3.0 or higher to be properly installed and configured. When installing the ``djangocms-instagram`` using pip, ``django-connected`` will also be installed automatically.

Preview
--------

.. image:: http://mishbahr.github.io/assets/djangocms-instagram/thumbnail/djangocms-instagram-001.png
  :target: http://mishbahr.github.io/assets/djangocms-instagram/djangocms-instagram-001.png
  :width: 768px
  :align: center


.. image:: http://mishbahr.github.io/assets/djangocms-instagram/thumbnail/djangocms-instagram-002.png
  :target: http://mishbahr.github.io/assets/djangocms-instagram/djangocms-instagram-002.png
  :width: 768px
  :align: center

.. image:: http://mishbahr.github.io/assets/djangocms-instagram/thumbnail/djangocms-instagram-003.png
  :target: http://mishbahr.github.io/assets/djangocms-instagram/djangocms-instagram-003.png
  :width: 480px
  :align: center


Quickstart
----------

1. Install ``djangocms-instagram``::

    pip install djangocms-instagram

2. Add ``djangocms_instagram`` to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'connected_accounts',
        'connected_accounts.providers',
        'djangocms_instagram',
        ...
    )


3. To enable ``Instagram`` as a provider for ``django-connected``::

    CONNECTED_ACCOUNTS_INSTAGRAM_CONSUMER_KEY = '<instagram_client_id>'
    CONNECTED_ACCOUNTS_INSTAGRAM_CONSUMER_SECRET = '<instagram_client_secret>'

4. Sync database (requires ``south>=1.0.1`` if you are using Django 1.6.x)::

    python manage.py migrate



Configuration
--------------

Plugin(s) Module - If module is None, plugin is grouped Generic group::

    DJANGOCMS_INSTAGRAM_PLUGIN_MODULE = _('Generic')

Name of the plugin::

    DJANGOCMS_INSTAGRAM_PLUGIN_NAME = _('Instagram')

Can this plugin only be attached to a placeholder that is attached to a page::

    DJANGOCMS_INSTAGRAM_PAGE_ONLY = False

A list of Plugin Class Names. If this is set, this plugin may only be added to plugins listed here::

    DJANGOCMS_INSTAGRAM_PARENT_CLASSES = None

Is it required that this plugin is a child of another plugin? Or can it be added to any placeholder::

    DJANGOCMS_INSTAGRAM_REQUIRE_PARENT = False

Whether this plugin can be used in text plugins or not::

    DJANGOCMS_INSTAGRAM_TEXT_ENABLED = False

The path to the default template used to render the template::

   DJANGOCMS_INSTAGRAM_DEFAULT_TEMPLATE = 'djangocms_instagram/default.html'

or override the ``Design`` dropdown choices to have different design options::

    DJANGOCMS_INSTAGRAM_TEMPLATES = (
        ('djangocms_instagram/default.html', _('Default')),
    )


You may also like...
--------------------

* djangocms-disqus - https://github.com/mishbahr/djangocms-disqus
* djangocms-fbcomments - https://github.com/mishbahr/djangocms-fbcomments
* djangocms-forms — https://github.com/mishbahr/djangocms-forms
* djangocms-gmaps — https://github.com/mishbahr/djangocms-gmaps
* djangocms-responsive-wrapper — https://github.com/mishbahr/djangocms-responsive-wrapper
* djangocms-twitter2 — https://github.com/mishbahr/djangocms-twitter2
* djangocms-youtube — https://github.com/mishbahr/djangocms-youtube
