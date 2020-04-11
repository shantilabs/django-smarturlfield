
from urllib.parse import urlparse, urlunparse


def force_punycode_domain_name(s):
    """
    Converts human-readable IDN domain to punycode.
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
    """
    Converts punycode hostname to human-readable name.
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
    """
    Convert domain name of given URL to punycode.
    """
    if not url:
        return url
    scheme, netloc, path, params, query, fragment = urlparse(url)
    netloc = force_punycode_domain_name(netloc)
    data = scheme, netloc, path, params, query, fragment
    return urlunparse(data)
