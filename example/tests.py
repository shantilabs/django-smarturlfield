# -*- coding: utf-8 -*-
from django import forms
from django.test import TestCase
from example.models import OneUrlModel, ManyUrlsModel


class UrlsTestCase(TestCase):
    def test_one_url(self):
        class F(forms.ModelForm):
            class Meta:
                model = OneUrlModel

        form = F({'url': 'ya.RU'})
        instance = form.save()

        self.assertEquals(instance.url, 'http://ya.ru/')

    def test_many_urls(self):
        class F(forms.ModelForm):
            class Meta:
                model = ManyUrlsModel

        form = F({'urls': 'ya.RU, xx.com '
                          'httP://zzz.ff'})
        self.assertTrue(form.is_valid(), form.as_p())
        instance = form.save()

        self.assertEquals(instance.urls, [
            u'http://xx.com',
            u'http://ya.ru',
            u'http://zzz.ff',
        ])

        form = F(instance=instance)
        self.assertFalse(form.errors, unicode(form))