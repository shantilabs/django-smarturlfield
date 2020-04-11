from django.db import models

from smarturlfield.formfields import MultipleSmartURLFormField, SmartURLFormField

__all__ = ['MultipleSmartURLDbField', 'SmartURLDbField']


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