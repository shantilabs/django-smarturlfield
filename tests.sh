#!/bin/bash
set -e
DJANGO_SETTINGS_MODULE=example.settings django-admin.py test --pythonpath=./ --failfast
python smarturlfield/__init__.py
