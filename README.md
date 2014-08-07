django-smarturlfield
====================

Allow enter url without "http://"

Install:
```
pip install git+https://github.com/shantilabs/django-smarturlfield#egg=smarturlfield
```

Forms:
```python
from smarturlfield import SmartURLDbField, SmartURLFormField

class MyForm(forms.Form):
    url = SmartURLFormField()
    # ...
```

Models:
```python
from smarturlfield import SmartURLDbField

class MyModel(models.Model):
    url = SmartURLDbField()
    # ...
```
