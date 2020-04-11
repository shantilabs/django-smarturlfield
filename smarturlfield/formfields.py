import re

from django import forms
from django.conf import settings
from django.core import validators
from django.forms import Textarea, TextInput
from django.utils.translation import ugettext_lazy

from .idn import force_punicode_url
from .utils import normalize_url


__all__ = ['MultipleSmartURLFormField', 'SmartURLFormField']


class MultipleSmartURLFormField(forms.CharField):
    widget = Textarea
    split_regex = re.compile(r';|,\s*|\s+')

    default_error_messages = {
        'invalid': ugettext_lazy('Enter a valid URL.'),
    }

    default_validators = [validators.URLValidator()]

    def to_python(self, value):
        if not value:
            return []
        lines = [force_punicode_url(normalize_url(x)) for x in self.split_regex.split(value)]
        lines = [line for line in sorted(set(lines)) if line]

        return lines

    def clean(self, value):
        value = self.to_python(value)
        for url in value:
            self.validate(url)
            self.run_validators(url)
        return value
        # return '\n'.join(value)

    def prepare_value(self, value):
        if isinstance(value, list):
            return '\n'.join(value)
        return value


class SmartURLFormField(forms.URLField):
    widget = TextInput

    def clean(self, value):
        if getattr(settings, 'SMARTURL_FIELD_EXTRA_VALID_URLS', None):
            for pattern in settings.SMARTURL_FIELD_EXTRA_VALID_URLS:
                if value == pattern:
                    return value
        if value:
            value = normalize_url(value)
        value = super(SmartURLFormField, self).clean(value)
        return force_punicode_url(value)