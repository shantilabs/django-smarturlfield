#!/bin/bash
set -e
python smarturlfield/__init__.py
DJANGO_SETTINGS_MODULE=example.settings django-admin.py test --pythonpath=./
