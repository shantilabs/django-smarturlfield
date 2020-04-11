def normalize_url(s):
    s = s.strip()
    if '://' in s or not s:
        return s
    else:
        return 'http://' + s
