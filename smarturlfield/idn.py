# -*- coding: utf-8 -*-
import urlparse


def force_punycode_domain_name(s):
    u"""
    >>> force_punycode_domain_name('xn--80ajfftz0a.xn--p1ai')
    'xn--80ajfftz0a.xn--p1ai'
    >>> force_punycode_domain_name('земфира.рф')
    'xn--80ajfftz0a.xn--p1ai'
    >>> force_punycode_domain_name('d56.ru')
    'd56.ru'
    """
    if s is None:
        return s

    s = s.lower().strip()
    if s.startswith('xn--'):
        return s
    else:
        try:
            return s.encode('idna')
        except TypeError:
            return s.decode('utf-8').encode('idna')


def force_punicode_url(url):
    u"""
    >>> force_punicode_url('https://земфира.рф/page1/')
    'https://xn--80ajfftz0a.xn--p1ai/page1/'
    """
    scheme, netloc, url, params, query, fragment = urlparse.urlparse(url)
    netloc = force_punycode_domain_name(netloc)
    data = scheme, netloc, url, params, query, fragment
    if url == '/':
        url = ''
    return urlparse.urlunparse(data)
