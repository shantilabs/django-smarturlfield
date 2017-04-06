from django.db import models
import smarturlfield


class OneUrlModel(models.Model):
    url = smarturlfield.SmartURLDbField()

    class Meta:
        app_label = 'example'


class ManyUrlsModel(models.Model):
    urls = smarturlfield.MultipleSmartURLDbField()

    class Meta:
        app_label = 'example'



