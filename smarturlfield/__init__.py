# -*- coding: utf-8 -*-
import re
from django.forms import TextInput, Textarea
from django.utils import six
from django.utils.encoding import smart_text


if __name__ == '__main__':
    from django.conf import settings
    if not settings.configured:
        settings.configure()


from django import forms
from django.db import models
from idn import force_punicode_url


class MultipleSmartURLFormField(forms.URLField):
    u"""
    >>> class Form(forms.Form):
    ...     urls = MultipleSmartURLFormField()
    >>> f = Form({'urls': u'''земфира.рф
    ... http://ya.ru,zzzz.com
    ... YA.ru
    ... '''})
    >>> f.is_valid()
    True
    >>> print f.cleaned_data['urls']
    http://xn--80ajfftz0a.xn--p1ai
    http://ya.ru
    http://zzzz.com
    """
    widget = Textarea
    split_regex = re.compile('[,\s]')

    def clean(self, value):
        if value:
            lines = [force_punicode_url(normalize_url(x)) for x in self.split_regex.split(value)]
            lines = filter(None, sorted(set(lines)))
            return '\n'.join(x for x in lines if x)
        else:
            return ''


class SmartURLFormField(forms.URLField):
    u"""
    >>> class Form(forms.Form):
    ...     url = SmartURLFormField()
    >>> Form({'url': '            '}).is_valid()
    False
    >>> Form({'url': 'ya.ru '}).is_valid()
    True
    >>> Form({'url': ' http://ya.ru '}).is_valid()
    True
    >>> Form({'url': u'http://домен.рф '}).is_valid()
    True
    >>> Form({'url': u'домен.рф '}).is_valid()
    True
    >>> f = Form({'url': u'земфира.рф'})
    >>> f.is_valid()
    True
    >>> f.cleaned_data['url']
    u'http://xn--80ajfftz0a.xn--p1ai/'
    """
    widget = TextInput

    def clean(self, value):
        if value:
            value = normalize_url(value)
        value = super(SmartURLFormField, self).clean(value)
        return force_punicode_url(value)


class SmartURLDbField(models.URLField):
    _max_length = 200
    _options = None

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = self._max_length
        self._options = (args, kwargs)
        super(SmartURLDbField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['form_class'] = SmartURLFormField
        return super(SmartURLDbField, self).formfield(**kwargs)

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = 'django.db.models.fields.URLField'
        args, kwargs = introspector(models.CharField(*self._options[0], **self._options[1]))
        kwargs['max_length'] = self._max_length
        return field_class, args, kwargs


class MultipleSmartURLDbField(models.TextField):
    _options = None

    def __init__(self, *args, **kwargs):
        self._options = (args, kwargs)
        super(MultipleSmartURLDbField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['form_class'] = MultipleSmartURLFormField
        return super(MultipleSmartURLDbField, self).formfield(**kwargs)

    def to_python(self, value):
        return value.split('\n') if value else []

    def get_prep_value(self, value):
        if isinstance(value, six.string_types):
            return u'\n'.join(value)
        elif value is None:
            return value
        else:
            return smart_text(value)

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = 'django.db.models.fields.TextField'
        args, kwargs = introspector(models.TextField(*self._options[0], **self._options[1]))
        return field_class, args, kwargs


def normalize_url(s):
    s = s.strip().lower()
    if '://' in s or not s:
        return s
    else:
        return u'http://' + s


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print 'tests passed'
