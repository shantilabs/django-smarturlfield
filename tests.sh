#!/bin/bash
set -e
DJANGO_SETTINGS_MODULE=example.settings django-admin.py test --pythonpath=./ --failfast
DJANGO_SETTINGS_MODULE=example.settings python smarturlfield/__init__.py
