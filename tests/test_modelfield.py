# coding: utf-8
from django import forms

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


def test_one_url(db):
    class F(forms.ModelForm):
        class Meta:
            model = OneUrlModel
            fields = '__all__'

    form = F({'url': 'ya.RU'})
    instance = form.save()

    assert instance.url == 'http://ya.ru'


def test_many_urls(db):
    class F(forms.ModelForm):
        class Meta:
            model = ManyUrlsModel
            fields = '__all__'

    form = F({'urls': 'ya.RU, xx.com '
                      'httP://zzz.ff'})

    assert form.is_valid()

    instance = form.save()

    assert instance.urls == [
        u'http://xx.com',
        u'http://ya.ru',
        u'http://zzz.ff',
    ]

    form = F(instance=instance)
    assert bool(form.errors) == False


def test_model(db):
    instance = ManyUrlsModel.objects.create(
        urls=['http://ya.ru', 'http://xx.com'],
    )

    assert ManyUrlsModel.objects.get(id=instance.id).urls == ['http://ya.ru', 'http://xx.com']

    instance = ManyUrlsModel.objects.create(
        urls='http://ya.ru',
    )

    assert ManyUrlsModel.objects.get(id=instance.id).urls == ['http://ya.ru']
