# -*- coding: utf-8 -*-
from django.db import models
import smarturlfield


class OneUrlModel(models.Model):
    url = smarturlfield.SmartURLDbField()


class ManyUrlsModel(models.Model):
    urls = smarturlfield.MultipleSmartURLDbField()
