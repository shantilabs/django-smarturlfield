# coding: utf-8

import pytest
from django.forms import Form
from smarturlfield import SmartURLFormField, MultipleSmartURLFormField

@pytest.mark.parametrize('url,is_valid', [
    (u'            ', False),
    (u'ya.ru       ', True),
    (u' http://ya.ru ', True),
    (u'http://домен.рф ', True),
    (u'домен.рф ', True),
    ])
def test_formfield_basic(url, is_valid):
    class TestForm(Form):
        url = SmartURLFormField()

    form = TestForm({'url': url})

    assert form.is_valid() == is_valid, form.errors.as_text()


def test_formfield_punycode():
    class TestForm(Form):
        url = SmartURLFormField()

    form = TestForm({'url': u'земфира.рф'})

    assert form.is_valid()
    assert form.cleaned_data['url'] == u'http://xn--80ajfftz0a.xn--p1ai'



def test_multi_formfield():
    class TestForm(Form):
        urls = MultipleSmartURLFormField()

    form = TestForm({'urls': u'''земфира.рф
    http://ya.ru,zzzz.com
    YA.ru
    '''})

    assert form.is_valid()
    assert form.cleaned_data['urls'] == [u'http://xn--80ajfftz0a.xn--p1ai', u'http://ya.ru', u'http://zzzz.com']
