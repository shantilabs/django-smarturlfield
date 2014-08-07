# -*- coding: utf-8 -*-
from django.forms import TextInput

if __name__ == '__main__':
    from django.conf import settings
    if not settings.configured:
        settings.configure()


from django import forms
from django.db import models
from idn import force_punicode_url


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
            value = value.strip().lower()
            if (
                not value.startswith('http://') and
                not value.startswith('https://')
            ):
                value = u'http://' + value
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print 'tests passed'
