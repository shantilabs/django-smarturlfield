django-smarturlfield
====================

Django model and form fields that performs URL normalization. For example it adds 'http://" prefix and forces punicode encoding.

Install:
```
pip install git+https://github.com/shantilabs/django-smarturlfield#egg=smarturlfield
```

Forms:
```python
from smarturlfield import SmartURLFormField, MultipleSmartURLFormField

class MyForm(forms.Form):
    url = SmartURLFormField()
    url_list = MultipleSmartURLFormField()  # textarea
    # ...
```

Models:
```python
from smarturlfield import SmartURLDbField, MultipleSmartURLDbField

class MyModel(models.Model):
    url = SmartURLDbField()
    url_list = MultipleSmartURLDbField()  # textarea
    # ...
```
