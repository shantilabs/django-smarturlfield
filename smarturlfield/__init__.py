import re

from django import forms
from django.db import models
from django.conf import settings
from django.core import validators
from django.forms import TextInput, Textarea
from django.utils.translation import ugettext_lazy

from .idn import force_punicode_url


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


class SmartURLDbField(models.URLField):
    description = "Smart URL Field"
    default_max_length = 200

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', self.default_max_length)
        super(SmartURLDbField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['form_class'] = SmartURLFormField
        return super(SmartURLDbField, self).formfield(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(SmartURLDbField, self).deconstruct()
        if kwargs.get('max_length') == self.default_max_length:
            kwargs.pop('max_length')
        return name, path, args, kwargs


class MultipleSmartURLDbField(models.TextField):
    description = "Multiple smart URLs field"

    def formfield(self, **kwargs):
        kwargs['form_class'] = MultipleSmartURLFormField
        return super(MultipleSmartURLDbField, self).formfield(**kwargs)

    def get_prep_value(self, value):
        if isinstance(value, str):
            return value
        elif isinstance(value, list):
            return '\n'.join(value)

    def from_db_value(self, value, expression, connection):
        return value.splitlines()

    def to_python(self, value):
        if isinstance(value, str):
            return value.splitlines()
        else:
            return value


def normalize_url(s):
    s = s.strip()
    if '://' in s or not s:
        return s
    else:
        return u'http://' + s
