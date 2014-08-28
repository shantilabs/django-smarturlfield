DEBUG = True
TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database.sqlite',
    }
}

STATIC_ROOT = ''
STATIC_URL = '/static/'

SECRET_KEY = '123'

#ROOT_URLCONF = 'example.urls'
#WSGI_APPLICATION = 'example.wsgi.application'

INSTALLED_APPS = (
    'example',
    'smarturlfield',
)
