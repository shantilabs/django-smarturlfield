from io import open
from os import path

import setuptools
from distutils.core import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-smarturlfield',
    version='1.1.1',
    author='Maxim Oransky',
    author_email='maxim.oransky@gmail.com',
    description="Django model and form fields that performs URL normalization. For example it adds 'http://' prefix and forces punicode encoding.",
    long_description=long_description,
    url='https://github.com/shantilabs/django-smarturlfield',
    packages=[
        'smarturlfield'
    ],
    keywords=[
        'django', 'django-fields', 'url'
    ],
    classifiers=[
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 1.9',
        'Framework :: Django',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
