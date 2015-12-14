# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from functools import partial

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from connected_accounts.admin import ConnectedAccountAdminMixin
from django.contrib import admin
from django.contrib.admin.options import IS_POPUP_VAR
from django.shortcuts import get_object_or_404
from django.template.loader import select_template
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from instagram import InstagramAPI, InstagramAPIError, InstagramClientError

from .conf import settings
from .forms import InstagramForm, LocationsLookupForm, UsersLookupForm
from .models import Instagram
from .widgets import LocationsLookupWidget, UserLookupWidget

logger = logging.getLogger('djangocms_instagram')


class InstagramPlugin(ConnectedAccountAdminMixin, CMSPluginBase):
    model = Instagram
    cache = False
    form = InstagramForm

    module = settings.DJANGOCMS_INSTAGRAM_PLUGIN_MODULE
    name = settings.DJANGOCMS_INSTAGRAM_PLUGIN_NAME
    render_template = settings.DJANGOCMS_INSTAGRAM_DEFAULT_TEMPLATE

    text_enabled = settings.DJANGOCMS_INSTAGRAM_TEXT_ENABLED
    page_only = settings.DJANGOCMS_INSTAGRAM_PAGE_ONLY
    require_parent = settings.DJANGOCMS_INSTAGRAM_REQUIRE_PARENT
    parent_classes = settings.DJANGOCMS_INSTAGRAM_PARENT_CLASSES

    fieldsets = (
        (None, {
            'fields': ('account',)
        }),
        (None, {
            'classes': ('media-source', ),  # used for custom styling.
            'fields': ('source', 'user_id', 'hashtag', 'location_id', )
        }),
        (None, {
            'fields': ('no_of_items', 'plugin_template', )
        }),
    )

    def get_render_template(self, context, instance, placeholder):
        # returns the first template that exists, falling back to bundled template
        return select_template([
            instance.plugin_template,
            settings.DJANGOCMS_INSTAGRAM_DEFAULT_TEMPLATE,
            'djangocms_instagram/default.html'
        ])

    def get_model_info(self):
        # module_name is renamed to model_name in Django 1.8
        app_label = self.model._meta.app_label
        try:
            return app_label, self.model._meta.model_name
        except AttributeError:
            return app_label, self.model._meta.module_name

    def get_form(self, request, obj=None, **kwargs):
        kwargs['formfield_callback'] = partial(self.formfield_for_dbfield, obj=obj)
        return super(InstagramPlugin, self).get_form(request, obj, **kwargs)

    def get_plugin_urls(self):
        from django.conf.urls import patterns, url
        info = self.get_model_info()

        return patterns(
            '',
            url(r'^locations/search/$',
                admin.site.admin_view(self.locations_search),
                name='%s_%s_locations_search' % info),
            url(r'^users/search/$',
                admin.site.admin_view(self.users_search),
                name='%s_%s_users_search' % info),
        )

    def get_api(self, request):
        if not hasattr(self, '_api'):
            rel_to = self.model._meta.get_field('account').rel.to
            connected_account = get_object_or_404(rel_to, pk=request.GET.get('account'))
            self._api = InstagramAPI(
                client_id=settings.CONNECTED_ACCOUNTS_INSTAGRAM_CONSUMER_KEY,
                client_secret=settings.CONNECTED_ACCOUNTS_INSTAGRAM_CONSUMER_SECRET,
                access_token=connected_account.get_token())
        return self._api

    def locations_search(self, request):
        api = self.get_api(request)
        errors = None

        try:
            results = api.location_search(
                lat=request.GET.get('lat', ''),
                lng=request.GET.get('lng', ''),
                count=20,
                distance=2000,
            )
        except (InstagramAPIError, InstagramClientError) as e:
            msg = _('Failed location lookup: LatLng({lat}, {lng}) - Reason: {error}').format(
                lat=request.GET.get('lat', ''), lng=request.GET.get('lng', ''), error=e)
            logger.error(msg)

            errors = e.error_message
            results = None

        search_form = LocationsLookupForm(initial=dict(request.GET.items()))

        context = dict(
            title=_('Location Search'),
            search_form=search_form,
            result_headers=('Location ID', 'Name', ),
            results=results,
            errors=errors,
        )

        return self.render_lookup_view(request, context, locations=True)

    def users_search(self, request):
        api = self.get_api(request)
        errors = None

        try:
            results = api.user_search(
                q=request.GET.get('username'),
                count=20,
            )
        except (InstagramAPIError, InstagramClientError) as e:
            msg = _('Failed user lookup: {username} - Reason: {error}').format(
                username=request.GET.get('username'), error=e)
            logger.error(msg)

            errors = e.error_message
            results = None

        search_form = UsersLookupForm(initial=dict(request.GET.items()))
        context = dict(
            title=_('Users Search'),
            search_form=search_form,
            result_headers=('User ID', 'Full Name', 'Username', ),
            results=results,
            errors=errors,
        )

        return self.render_lookup_view(request, context, users=True)

    def render_lookup_view(self, request, context, form_url='', locations=False, users=False):
        context.update({
            'is_popup': IS_POPUP_VAR in request.GET,
            'form_url': form_url,
            'opts': self.model._meta,
            'users': users,
            'locations': locations,
        })
        return TemplateResponse(request, 'admin/djangocms_instagram/search.html', context)

    def icon_src(self, instance):
        return settings.STATIC_URL + 'admin/img/djangocms_instagram/instagram_icon.png'

    def formfield_for_dbfield(self, db_field, **kwargs):
        db = kwargs.get('using')
        obj = kwargs.pop('obj', None)

        if db_field.name in ('location_id', 'user_id'):
            if db_field.name == 'location_id':
                kwargs['widget'] = LocationsLookupWidget(obj, self.admin_site, using=db)
            elif db_field.name == 'user_id':
                kwargs['widget'] = UserLookupWidget(obj, self.admin_site, using=db)

            return db_field.formfield(**kwargs)
        return super(InstagramPlugin, self).formfield_for_dbfield(db_field, **kwargs)

    class Media:
        css = {
            'all': (
                'admin/css/djangocms_instagram/djangocms_instagram.css',
            )
        }
        js = ('admin/js/djangocms_instagram/djangocms_instagram.js', )

plugin_pool.register_plugin(InstagramPlugin)
