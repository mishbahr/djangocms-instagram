# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from cms.models import CMSPlugin
from connected_accounts.fields import AccountField
from django.core.cache import cache
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from instagram import InstagramAPI, InstagramAPIError, InstagramClientError

from .conf import settings

try:
    from urllib.parse import parse_qs, urlparse
except ImportError:  # pragma: no cover
    # Python 2.X
    from urlparse import parse_qs, urlparse


logger = logging.getLogger('djangocms_instagram')

ERROR_VAR = '_error'


@python_2_unicode_compatible
class Instagram(CMSPlugin):
    MEDIA_SOURCE_FEED = 'feed'
    MEDIA_SOURCE_LIKE = 'like'
    MEDIA_SOURCE_TAG = 'tag'
    MEDIA_SOURCE_LOCATION = 'location'

    MEDIA_SOURCE_CHOICES = (
        (MEDIA_SOURCE_FEED, _('Media published by the user')),
        (MEDIA_SOURCE_TAG, _('Media tagged with a given tag')),
        (MEDIA_SOURCE_LOCATION, _('Media from a given location')),
        (MEDIA_SOURCE_LIKE, _('Media liked by the connected user')),
    )
    account = AccountField(
        'instagram', verbose_name=_('Connected Account'),
        help_text=_('Select a connected Instagram account or connect to a new account.'))
    no_of_items = models.IntegerField(
        _('Items to Display'), default=10,
        help_text=_('Select the number of items this plugin should display'))
    plugin_template = models.CharField(
        _('Design'), max_length=150,
        choices=settings.DJANGOCMS_INSTAGRAM_TEMPLATES,
        default=settings.DJANGOCMS_INSTAGRAM_DEFAULT_TEMPLATE,
    )
    source = models.CharField(
        _('Media Source'), max_length=50,
        choices=MEDIA_SOURCE_CHOICES, default=MEDIA_SOURCE_FEED)

    location_id = models.CharField(
        _('Location ID'), max_length=50, blank=True,
        help_text=_('Get a list of recent media objects from a given location.'))
    user_id = models.CharField(
        _('User ID'), max_length=50, blank=True,
        help_text=_('By default, display the most recent media published by the connected user'))
    hashtag = models.CharField(
        _('Hashtag'), max_length=50, blank=True,
        help_text=_('Get a list of recent media objects from a given tag.'))

    def __str__(self):
        if self.source == self.MEDIA_SOURCE_FEED:
            profile_data = self.get_profile()
            if ERROR_VAR in profile_data:
                return _('Error: {error}').format(error=profile_data.get(ERROR_VAR))

            name = profile_data.get('full_name')
            username = profile_data.get('username')
            return _('Photos/Videos published by {name} ({username})').format(
                name=name, username=username)

        if self.source == self.MEDIA_SOURCE_LIKE:
            profile_data = self.get_profile(user_id=self.account.uid)
            if ERROR_VAR in profile_data:
                return _('Error: {error}').format(error=profile_data.get(ERROR_VAR))

            name = profile_data.get('full_name')
            username = profile_data.get('username')
            return _('Photos/Videos liked by {name} ({username})').format(
                name=name, username=username)

        if self.source == self.MEDIA_SOURCE_LOCATION:
            location_data = self.get_location()
            if ERROR_VAR in location_data:
                return _('Error: {error}').format(error=location_data.get(ERROR_VAR))
            else:
                return _('Photos/Videos from {name}').format(name=location_data.get('name', ''))

        if self.source == self.MEDIA_SOURCE_TAG:
            return _('Photos/Videos about #{tag}').format(tag=self.hashtag.lstrip('#').strip())

    def save(self, *args, **kwargs):
        super(Instagram, self).save(*args, **kwargs)
        cache_keys = (
            self.get_cache_key(prefix='profile_%s' % self.user_id.strip()),
            self.get_cache_key(prefix='profile_%s' % self.account.uid),
            self.get_cache_key(prefix='location_%s' % self.location_id.strip()),
            self.get_cache_key(prefix='media'),
        )
        cache.delete_many(cache_keys)

    def get_api(self):
        if not hasattr(self, '_api'):
            self._api = InstagramAPI(
                client_id=settings.CONNECTED_ACCOUNTS_INSTAGRAM_CONSUMER_KEY,
                client_secret=settings.CONNECTED_ACCOUNTS_INSTAGRAM_CONSUMER_SECRET,
                access_token=self.account.get_token())
        return self._api

    def get_cache_key(self, prefix=''):
        return 'djangocms-instagram-{prefix}-{id}'.format(prefix=prefix, id=str(self.id))

    def get_profile(self, user_id=None):
        if not user_id:
            alternative_user = self.user_id.strip()
            if alternative_user and self.source == self.MEDIA_SOURCE_FEED:
                user_id = alternative_user
            else:
                user_id = self.account.uid

        cache_key = self.get_cache_key(prefix='profile_{user_id}'.format(user_id=user_id))

        data = cache.get(cache_key) or {}

        if not data:
            api = self.get_api()
            data = {
                'user_id': user_id,
            }

            try:
                data = api.user(user_id)
            except (InstagramAPIError, InstagramClientError) as e:
                msg = _('Failed to retrieve information '
                        'for user-id: {user_id} - Reason: {error}').format(
                    user_id=user_id, error=e)
                logger.error(msg)
                data[ERROR_VAR] = str(e.error_message)
            else:
                data = {
                    'username': getattr(data, 'username', ''),
                    'profile_picture': getattr(data, 'profile_picture', ''),
                    'full_name': getattr(data, 'full_name', ''),
                    'user_id': getattr(data, 'id', ''),
                    'media_count': getattr(data, 'counts', {}).get('media', 0),
                    'followers_count': getattr(data, 'counts', {}).get('followed_by', 0),
                    'following_count': getattr(data, 'counts', {}).get('follows', 0),
                }
                cache.set(cache_key, data, settings.DJANGOCMS_INSTAGRAM_CACHE_DURATION)

        return data

    def get_location(self, location_id=None):
        if not location_id:
            location_id = self.location_id.strip()

        cache_key = self.get_cache_key(prefix='location_{location_id}'.format(
            location_id=location_id))
        data = cache.get(cache_key) or {}

        if not data:
            api = self.get_api()
            data = {
                'location_id': location_id,
            }

            try:
                location = api.location(location_id)
            except (InstagramAPIError, InstagramClientError) as e:
                msg = _('Failed to retrieve information '
                        'for location ID: {location_id} - Reason: {error}').format(
                    location_id=location_id, error=e)
                logger.error(msg)
                data[ERROR_VAR] = str(e.error_message)
            else:
                data = {
                    'location_id': getattr(location, 'id', ''),
                    'name': getattr(location, 'name', ''),
                }

                point = getattr(location, 'point')
                data.update({
                    'latitude': getattr(point, 'latitude'),
                    'longitude': getattr(point, 'longitude'),
                })

                cache.set(cache_key, data, settings.DJANGOCMS_INSTAGRAM_CACHE_DURATION)

        return data

    def get_max_id(self, url, key='max_id'):
        url_parts = urlparse(url)
        return parse_qs(url_parts.query)[key][0]

    def get_media(self):
        cache_key = self.get_cache_key(prefix='media')
        media = cache.get(cache_key)

        if not media:
            api = self.get_api()
            media = []
            try:
                if self.source == self.MEDIA_SOURCE_FEED:
                    user_id = self.user_id.strip() or self.account.uid
                    media_feed, next = api.user_recent_media(
                        user_id=user_id, count=self.no_of_items)
                    media.extend(media_feed)
                    while next and len(media) < self.no_of_items:
                        max_id = self.get_max_id(next)
                        media_feed, next = api.user_recent_media(
                            user_id=user_id, max_id=max_id)
                        media.extend(media_feed)

                elif self.source == self.MEDIA_SOURCE_LIKE:
                    media_feed, next = api.user_liked_media(count=self.no_of_items)
                    media.extend(media_feed)
                    while next and len(media) < self.no_of_items:
                        max_id = self.get_max_id(next)
                        media_feed, next = api.user_liked_media(max_id=max_id)
                        media.extend(media_feed)

                elif self.source == self.MEDIA_SOURCE_LOCATION:
                    media_feed, next = api.location_recent_media(
                        location_id=self.location_id.strip(), count=self.no_of_items)
                    media.extend(media_feed)
                    while next and len(media) < self.no_of_items:
                        max_id = self.get_max_id(next)
                        media_feed, next = api.location_recent_media(
                            location_id=self.location_id.strip(), max_id=max_id)
                        media.extend(media_feed)

                elif self.source == self.MEDIA_SOURCE_TAG:
                    media_feed, next = api.tag_recent_media(
                        tag_name=self.hashtag.strip(), count=self.no_of_items)
                    media.extend(media_feed)
                    while next and len(media) < self.no_of_items:
                        max_tag_id = self.get_max_id(next, key='max_tag_id')
                        media_feed, next = api.tag_recent_media(
                            tag_name=self.hashtag.strip(), max_tag_id=max_tag_id)
                        media.extend(media_feed)

            except (InstagramAPIError, InstagramClientError) as e:
                msg = _('Failed to retrieve media - Reason: {error}').format(error=e)
                logger.error(msg)
            else:
                cache.set(cache_key, media, settings.DJANGOCMS_INSTAGRAM_CACHE_DURATION)

        return media[:self.no_of_items]
