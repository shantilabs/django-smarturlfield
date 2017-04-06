# coding: utf-8
import pytest

from smarturlfield.idn import force_punycode_domain_name, force_readable_domain_name, force_punicode_url

@pytest.mark.parametrize('input_,output', [
    ('xn--80ajfftz0a.xn--p1ai', 'xn--80ajfftz0a.xn--p1ai'),
    (u'земфира.рф', 'xn--80ajfftz0a.xn--p1ai'),
    ('d56.ru', 'd56.ru'),
    (u'中国互联网络信息中心.中国', 'xn--fiqa61au8b7zsevnm8ak20mc4a87e.xn--fiqs8s'),
    (None, None),
])
def test_punycode(input_, output):
    assert force_punycode_domain_name(input_) == output


@pytest.mark.parametrize('input_,output', [
    ('xn--80ajfftz0a.xn--p1ai', u'земфира.рф'),
    (u'земфира.рф', u'земфира.рф'),
    ('d56.ru', 'd56.ru'),
    ('xn--fiqa61au8b7zsevnm8ak20mc4a87e.xn--fiqs8s', u'中国互联网络信息中心.中国'),
    (None, None),
])
def test_readable(input_, output):
    assert force_readable_domain_name(input_) == output


def test_punicode_url():
    assert force_punicode_url('https://земфира.рф/page1/') == 'https://xn--80ajfftz0a.xn--p1ai/page1/'
