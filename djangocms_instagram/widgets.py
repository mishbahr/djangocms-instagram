# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django import forms
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .conf import settings
from .models import ERROR_VAR, Instagram

try:
    from urllib.parse import urlencode
except ImportError:  # pragma: no cover
    # Python 2.X
    from urllib import urlencode


logger = logging.getLogger('djangocms_instagram')


class InstagramLookupWidget(forms.TextInput):
    model = Instagram
    view_url_name = ''
    lookup_label = ''
    lookup_template = """
        <a href="{0}" class="instagram-search search" id="lookup_id_{1}" title="{2} lookup">
            <img src="{3}admin/img/djangocms_instagram/icon_searchbox.png" height="16" width="16">
        </a>
    """

    def __init__(self, model_instance, admin_site, attrs=None, using=None):
        self.model_instance = model_instance
        self.admin_site = admin_site
        self.db = using
        super(InstagramLookupWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}

        extra = []
        opts = self.model._meta

        app_label = opts.app_label
        try:
            model_name = opts.model_name
        except AttributeError:
            model_name = opts.module_name

        lookup_url = reverse(
            'admin:%s_%s_%s' % (
                app_label,
                model_name,
                self.view_url_name,
            ),
            current_app=self.admin_site.name,
        )

        query_params = self.get_query_params(value)
        url = '{0}?{1}'.format(lookup_url, urlencode(query_params))

        extra.append(self.lookup_template.format(
            url, name, self.lookup_label, settings.STATIC_URL))

        output = [super(InstagramLookupWidget, self).render(name, value, attrs)] + extra
        output.append(self.label_for_value(name, value))

        return mark_safe('<div class="instagram-lookup">{0}</div>'.format(''.join(output)))

    def label_for_value(self, name, value):
        if value is None:
            value = ''
        return '<span id="label_%s" class="label">%s</span>' % (name, value)


class UserLookupWidget(InstagramLookupWidget):
    view_url_name = 'users_search'
    lookup_label = _('User ID')

    def label_for_value(self, name, value):
        if self.model_instance and value:
            user = self.model_instance.get_profile(user_id=value)
            if ERROR_VAR in user:
                value = _('Error: {0}').format(user.get(ERROR_VAR))
            else:
                value = '{0} ({1})'.format(
                    user.get('full_name', ''),
                    user.get('username', ''),
                )
        return super(UserLookupWidget, self).label_for_value(name, value)

    def get_query_params(self, value):
        query = settings.DJANGOCMS_INSTAGRAM_USER_SEARCH_QUERY
        if self.model_instance and value:
            user = self.model_instance.get_profile(user_id=value)
            if ERROR_VAR not in user:
                query = user.get('username', user)
        return dict(
            username=query
        )


class LocationsLookupWidget(InstagramLookupWidget):
    view_url_name = 'locations_search'
    lookup_label = _('Location ID')

    def label_for_value(self, name, value):
        if self.model_instance and value:
            location = self.model_instance.get_location(location_id=value)
            if ERROR_VAR in location:
                value = _('Error: {0}').format(location.get(ERROR_VAR))
            else:
                value = location.get('name', '')
        return super(LocationsLookupWidget, self).label_for_value(name, value)

    def get_query_params(self, value):
        latitude = settings.DJANGOCMS_INSTAGRAM_LOCATION_SEARCH_QUERY_LATITUDE
        longitude = settings.DJANGOCMS_INSTAGRAM_LOCATION_SEARCH_QUERY_LONGITUDE

        if self.model_instance and value:
            location = self.model_instance.get_location(location_id=value)
            if ERROR_VAR not in location:
                latitude = location.get('latitude', latitude)
                longitude = location.get('longitude', longitude)

        return dict(
            lat=latitude,
            lng=longitude,
        )
