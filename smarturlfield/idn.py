# coding: utf-8
import sys

if sys.version_info > (3, 0):
    from urllib.parse import urlparse, urlunparse
else:
    from urlparse import urlparse, urlunparse


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
            result = s.encode('idna')
        except TypeError:
            result = s.decode('utf-8').encode('idna')
        return result.decode()  # return string (not bytes)


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
            s = s.encode()
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
    scheme, netloc, path, params, query, fragment = urlparse(url)
    netloc = force_punycode_domain_name(netloc)
    data = scheme, netloc, path, params, query, fragment
    return urlunparse(data)
