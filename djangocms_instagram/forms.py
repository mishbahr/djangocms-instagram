from django import forms
from django.contrib.admin.widgets import AdminRadioSelect
from django.utils.translation import ugettext_lazy as _

from .models import Instagram


class InstagramForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(InstagramForm, self).clean()

        media_source = cleaned_data.get('source')
        required_error_msg = _('This field is required.')

        if media_source == 'tag' and not cleaned_data.get('hashtag'):
            self._errors['hashtag'] = self.error_class([required_error_msg])

        if media_source == 'location' and not cleaned_data.get('location_id'):
            self._errors['location_id'] = self.error_class([required_error_msg])

        return cleaned_data

    class Meta:
        model = Instagram
        fields = '__all__'
        error_messages = {
            'account': {
                'required': _('A connected Instagram account is required for this plugin.'),
            },
        }
        widgets = {
            'source': AdminRadioSelect(attrs={'class': 'radiolist'}),
        }


class SearchForm(forms.Form):
    account = forms.CharField(widget=forms.HiddenInput())


class UsersLookupForm(SearchForm):
    username = forms.CharField(
        label=_('Name'),
        widget=forms.TextInput(attrs={'size': 40}))


class LocationsLookupForm(SearchForm):
    location = forms.CharField(
        label=_('Address'),
        widget=forms.TextInput(attrs={'size': 40}))
    lat = forms.CharField(label=_('Latitude'))
    lng = forms.CharField(label=_('longitude'))
