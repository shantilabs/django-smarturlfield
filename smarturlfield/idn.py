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


def force_readable_domain_name(s):
    u"""
    >>> res = u'земфира.рф'
    >>> res == force_readable_domain_name('xn--80ajfftz0a.xn--p1ai')
    True
    >>> res = 'земфира.рф'
    >>> res == force_readable_domain_name('земфира.рф')
    True
    >>> force_readable_domain_name('d56.ru')
    'd56.ru'
    """
    if s is None:
        return s

    s = s.lower().strip()
    if s.startswith('xn--') or '.xn--' in s:
        try:
            return s.decode('idna')
        except UnicodeError:
            return s
    else:
        return s


def force_punicode_url(url):
    u"""
    >>> force_punicode_url('https://земфира.рф/page1/')
    'https://xn--80ajfftz0a.xn--p1ai/page1/'
    """
    if not url:
        return url
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
    netloc = force_punycode_domain_name(netloc)
    data = scheme, netloc, path, params, query, fragment
    return urlparse.urlunparse(data)
