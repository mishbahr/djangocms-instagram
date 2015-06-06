# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import connected_accounts.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connected_accounts', '0001_initial'),
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instagram',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('no_of_items', models.IntegerField(default=10, help_text='Select the number of items this plugin should display', verbose_name='Items to Display')),
                ('plugin_template', models.CharField(default=b'djangocms_instagram/default.html', max_length=150, verbose_name='Design', choices=[(b'djangocms_instagram/default.html', 'Default')])),
                ('source', models.CharField(default='feed', max_length=50, verbose_name='Media Source', choices=[('feed', 'Media published by the user'), ('tag', 'Media tagged with a given tag'), ('location', 'Media from a given location'), ('like', 'Media liked by the connected user')])),
                ('location_id', models.CharField(help_text='Get a list of recent media objects from a given location.', max_length=50, verbose_name='Location ID', blank=True)),
                ('user_id', models.CharField(help_text='By default, display the most recent media published by the connected user', max_length=50, verbose_name='User ID', blank=True)),
                ('hashtag', models.CharField(help_text='Get a list of recent media objects from a given tag.', max_length=50, verbose_name='Hashtag', blank=True)),
                ('account', connected_accounts.fields.AccountField(verbose_name='Connected Account', to='connected_accounts.Account', provider='instagram', help_text='Select a connected Instagram account or connect to a new account.')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
