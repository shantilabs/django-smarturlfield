====================
django-smarturlfield
====================

Django model and form fields that performs URL normalization. For example it adds `'http://'` prefix and forces punicode encoding.
There are also fields that stores a list of URLs.

Tested with Django 1.11 and 2.1.

.. image:: https://travis-ci.org/shantilabs/django-smarturlfield.svg?branch=master
   :target: https://travis-ci.org/shantilabs/django-smarturlfield
   :alt: Travis-CI build status

Installing
==========

    $ pip install django-smarturlfield


Fields
======

**SmartURLFormField** renders as `<input>` and can handle values like this:
 
  - ``http://example.com``
  - `example.com` (normalized to ``http://example.com``)
  - `земфира.рф` (normalized to ``http://xn--80ajfftz0a.xn--p1ai``)

**MultipleSmartURLFormField** renders as `<textarea>` and can store multiple URLs separated by newline.


Usage
=====

In forms:

.. code-block:: python

    from smarturlfield import SmartURLFormField, MultipleSmartURLFormField

    class MyForm(forms.Form):
      url = SmartURLFormField()
      url_list = MultipleSmartURLFormField()  # textarea
      # ...

In models:

.. code-block:: python

    from smarturlfield import SmartURLDbField, MultipleSmartURLDbField

    class MyModel(models.Model):
        url = SmartURLDbField()
        url_list = MultipleSmartURLDbField()  # textarea
        # ...
