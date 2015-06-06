# -*- coding: utf-8 -*-

from appconf import AppConf
from django.conf import settings  # noqa
from django.utils.translation import ugettext_lazy as _


class DjangoCMSInstagramConf(AppConf):
    PLUGIN_MODULE = _('Generic')
    PLUGIN_NAME = _('Instagram')

    PAGE_ONLY = False
    PARENT_CLASSES = None
    REQUIRE_PARENT = False
    TEXT_ENABLED = False
    DEFAULT_TEMPLATE = 'djangocms_instagram/default.html'

    TEMPLATES = (
        ('djangocms_instagram/default.html', _('Default')),
    )

    CACHE_DURATION = 300  # 5 mins

    USER_SEARCH_QUERY = 'jack'
    LOCATION_SEARCH_QUERY_LATITUDE = '48.858729348'
    LOCATION_SEARCH_QUERY_LONGITUDE = '2.294340134'

    class Meta:
        prefix = 'djangocms_instagram'
